import json
import requests


class Instagram:

    def __init__(self, cookies):
        self.cookies = cookies
        self.session = requests.Session()
        self.headers = {
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
            'x-asbd-id': '359341',
            'x-csrftoken': self.cookies.get('csrftoken', ''),
            'x-ig-app-id': '936619743392459',
            'x-requested-with': 'XMLHttpRequest',
        }

    def follow(self, id):
        """Lấy danh sách người theo dõi (followers)."""
        params = {
            'count': '50',
            'search_surface': 'follow_list_page',
        }
        try:
            response = self.session.get(
                f'https://www.instagram.com/api/v1/friendships/{id}/followers/',
                params=params,
                cookies=self.cookies,
                headers=self.headers,
                timeout=15,
            )
            return response.json()
        except Exception as e:
            return {'status': 'fail', 'message': str(e)}

    def like(self, id):
        """Lấy danh sách tài khoản đã thích (likers) của media."""
        try:
            response = self.session.get(
                f'https://www.instagram.com/api/v1/media/{id}/likers/',
                cookies=self.cookies,
                headers=self.headers,
                timeout=15,
            )
            return response.json()
        except Exception as e:
            return {'status': 'fail', 'message': str(e)}

    def comment(self, media_id):
        """Lấy toàn bộ comment của bài viết qua API GraphQL Polaris bằng media_id."""
        url = 'https://www.instagram.com/graphql/query'
        params = {
            'doc_id': '28319576384320582',
            'variables': json.dumps({
                'media_id': str(media_id),
                '__relay_internal__pv__PolarisIsLoggedInrelayprovider': True,
            }),
        }

        try:
            self.headers['referer'] = 'https://www.instagram.com/p/instagram/'
            response = self.session.post(
                url,
                cookies=self.cookies,
                headers=self.headers,
                data=params,
                timeout=15,
            )
            return response.json()
        except Exception as e:
            return {'status': 'fail', 'message': str(e)}

    def _extract_comments(self, data):
        """Quét sâu vào response JSON để trích xuất đầy đủ thông tin comment."""
        comments = []
        if isinstance(data, dict):
            if 'user' in data and 'text' in data and isinstance(data.get('user'), dict):
                user_info = data.get('user') or {}
                user_pk = str(
                    user_info.get('pk') or user_info.get('id') or ''
                ).strip()
                username = str(user_info.get('username') or '').strip()
                text = str(data.get('text') or '').strip()
                comment_pk = str(data.get('pk') or data.get('id') or '').strip()

                if user_pk or username:
                    comments.append({
                        'comment_id': comment_pk,
                        'user_id': user_pk,
                        'username': username,
                        'text': text,
                        'created_at': data.get('created_at'),
                    })

            for v in data.values():
                if isinstance(v, (dict, list)):
                    comments.extend(self._extract_comments(v))

        elif isinstance(data, list):
            for item in data:
                comments.extend(self._extract_comments(item))

        unique_comments = []
        seen_ids = set()
        for c in comments:
            unique_key = c['comment_id'] or f"{c['user_id']}_{c['text']}"
            if unique_key not in seen_ids:
                seen_ids.add(unique_key)
                unique_comments.append(c)

        return unique_comments

    def _extract_all_ids(self, data):
        """Quét toàn bộ ID/PK trả về cho các tác vụ Like/Follow."""
        found_ids = set()
        if isinstance(data, dict):
            for k, v in data.items():
                if k.lower() in ('id', 'pk', 'pk_id', 'strong_id__', 'user_id') and v:
                    found_ids.add(str(v).strip())
                elif isinstance(v, (dict, list)):
                    found_ids.update(self._extract_all_ids(v))
        elif isinstance(data, list):
            for item in data:
                found_ids.update(self._extract_all_ids(item))
        return found_ids

    def check_list(
        self,
        target_id,
        user_list,
        response_data,
        check_type='comment',
        comment_text=None,
    ):
        """Kiểm tra danh sách user_list có nằm trong target_id (Follow, Like, Comment) hay không."""
        if not response_data or not isinstance(response_data, dict):
            return {
                'success': False,
                'type': check_type,
                'target_id': str(target_id),
                'message': 'Không nhận được response hoặc dữ liệu không hợp lệ.',
                'results': [],
            }

        target_id_str = str(target_id).strip()
        results = []

        # Xử lý kiểm tra cho từng user trong danh sách
        if check_type == 'comment':
            all_comments = self._extract_comments(response_data)
            for uid in user_list:
                uid_str = str(uid).strip()
                matched_comments = [
                    c for c in all_comments if c['user_id'] == uid_str
                ]
                is_exist = len(matched_comments) > 0

                if comment_text and is_exist:
                    is_exist = any(
                        comment_text.strip().lower() in c['text'].lower()
                        for c in matched_comments
                    )

                results.append({
                    'user_id': uid_str,
                    'is_active': is_exist,
                    'comments_found': matched_comments,
                })
        else:
            all_ids = self._extract_all_ids(response_data)
            for uid in user_list:
                uid_str = str(uid).strip()
                is_exist = uid_str in all_ids
                results.append({
                    'user_id': uid_str,
                    'is_active': is_exist,
                })

        return {
            'success': True,
            'type': check_type,
            'target_id': target_id_str,
            'results': results,
            'message': f'Đã kiểm tra danh sách người dùng cho mục {target_id_str}.',
        }