import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import random
import re
import time
from threading import Lock

print_lock = Lock()


def safe_log(msg):
    with print_lock:
        print(msg)


class Threads:

    def __init__(self, cookies):
        crf = re.search('csrftoken=([a-zA-Z0-9_-]+);', cookies).group(1)
        self.headers = {
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.com',
            'priority': 'u=1, i',
            'referer': 'https://www.threads.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': (
                '"Not;A=Brand";v="8", "Chromium";v="150",'
                ' "Google Chrome";v="150"'
            ),
            'sec-ch-ua-full-version-list': (
                '"Not;A=Brand";v="8.0.0.0", "Chromium";v="150.0.7871.101",'
                ' "Google Chrome";v="150.0.7871.101"'
            ),
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-model': '"Pixel 9"',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua-platform-version': '"15"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': (
                'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36'
            ),
            'x-asbd-id': '359341',
            'x-csrftoken': crf,
            'x-fb-friendly-name': 'useTHFollowMutationFollowMutation',
            'x-fb-lsd': 'Y-6rHZVy83JL--TA6d6l1V',
            'x-ig-app-id': '1412234116260832',
            'x-web-session-id': 'hajc5s:mswvxz:c36ovj',
            'cookie': cookies,
        }

    def data(self):
        response = requests.get(
            'https://www.threads.com/', headers=self.headers
        ).text
        actorID = re.search('"actorID":"([a-zA-Z0-9_-]+)"', response).group(1)
        dtsgID = re.search('"token":"([a-zA-Z0-9_:-]+)"', response).group(1)
        return actorID, dtsgID

    def follow(self, id):
        actorID, dtsgID = self.data()
        data = {
            'av': actorID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaFriendshipsFollowersTabQuery',
            'variables': (
                '{"first":20,"userID":"'
                + str(id)
                + '","__relay_internal__pv__BarcelonaIsInternalUserrelayprovider":false,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsCrawlerrelayprovider":false,"__relay_internal__pv__BarcelonaShouldShowFediverseListsrelayprovider":true}'
            ),
            'doc_id': '36970093975969258',
        }
        try:
            response = requests.post(
                'https://www.threads.com/graphql/query',
                headers=self.headers,
                data=data,
            ).json()
            return response
        except Exception:
            return {}

    def like(self, id):
        actorID, dtsgID = self.data()
        data = {
            'av': actorID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaFeedbackHubTabQuery',
            'variables': (
                '{"post_id":"'
                + str(id)
                + '","sort_type":"default","tab_type":"like","__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider":true,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaHasEventBadgerelayprovider":false,"__relay_internal__pv__BarcelonaHasWebFaviconsrelayprovider":false,"__relay_internal__pv__BarcelonaIsCrawlerrelayprovider":false,"__relay_internal__pv__BarcelonaHasCommunityTopContributorsrelayprovider":false}'
            ),
            'doc_id': '37728278513482268',
        }
        try:
            response = requests.post(
                'https://www.threads.com/graphql/query',
                headers=self.headers,
                data=data,
            ).json()
            return response
        except Exception:
            return {}

    def comment(self, id):
        actorID, dtsgID = self.data()
        data = {
            'av': actorID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': (
                'BarcelonaPostPageStrongIdDownwardQuery'
            ),
            'variables': (
                '{"filterType":"all","postID":"'
                + str(id)
                + '","sortOrder":"TOP","__relay_internal__pv__BarcelonaHasDearAlgoConsumptionrelayprovider":true,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaHasEventBadgerelayprovider":false,"__relay_internal__pv__BarcelonaGenAIRepliesEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaHasCommunitiesrelayprovider":true,"__relay_internal__pv__BarcelonaHasGameScoreSharerelayprovider":true,"__relay_internal__pv__BarcelonaHasPublicViewCountCardrelayprovider":true,"__relay_internal__pv__BarcelonaHasCommunityEmojiUpdateCardrelayprovider":false,"__relay_internal__pv__BarcelonaHasCommunityEntityCardrelayprovider":true,"__relay_internal__pv__BarcelonaHasScorecardCommunityrelayprovider":true,"__relay_internal__pv__BarcelonaHasSportTeamAllegianceCardrelayprovider":true,"__relay_internal__pv__BarcelonaHasMusicrelayprovider":true,"__relay_internal__pv__BarcelonaHasNewspaperLinkStylerelayprovider":false,"__relay_internal__pv__BarcelonaHasMessagingrelayprovider":true,"__relay_internal__pv__BarcelonaHasPodcastV2Consumptionrelayprovider":true,"__relay_internal__pv__BarcelonaHasPodcastTranscriptConsumptionrelayprovider":true,"__relay_internal__pv__BarcelonaShouldFulfillLightboxQueryrelayprovider":true,"__relay_internal__pv__BarcelonaHasViewerRepliedrelayprovider":true,"__relay_internal__pv__BarcelonaHasPrivateRepliesDeprecationrelayprovider":true,"__relay_internal__pv__BarcelonaHasGhostPostEmojiActivationrelayprovider":false,"__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider":true,"__relay_internal__pv__BarcelonaHasDearAlgoWebProductionrelayprovider":false,"__relay_internal__pv__BarcelonaHasWebFaviconsrelayprovider":false,"__relay_internal__pv__BarcelonaIsCrawlerrelayprovider":false,"__relay_internal__pv__BarcelonaHasCommunityTopContributorsrelayprovider":false,"__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider":false,"__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider":true,"__relay_internal__pv__BarcelonaIsInternalUserrelayprovider":false,"__relay_internal__pv__BarcelonaHasPermalinkIndentationrelayprovider":false}'
            ),
            'doc_id': '28399981646354979',
        }
        try:
            response = requests.post(
                'https://www.threads.com/api/graphql',
                headers=self.headers,
                data=data,
            ).json()
            return response
        except Exception:
            return {}

    def _extract_all_comments(self, data):
        """Duyệt đệ quy bóc tách danh sách các comment: {'user_id', 'username', 'text'}."""
        comments = []

        if isinstance(data, dict):
            user_obj = data.get('user')
            text_frags = data.get('text_fragments', {}).get('fragments', [])
            caption_obj = data.get('caption')

            user_id = ''
            username = ''
            text = ''

            if isinstance(user_obj, dict):
                user_id = str(
                    user_obj.get('pk')
                    or user_obj.get('id')
                    or user_obj.get('strong_id__')
                    or ''
                ).strip()
                username = str(user_obj.get('username', '')).strip()

            if text_frags:
                text = ''.join([
                    f.get('plaintext', '')
                    for f in text_frags
                    if isinstance(f, dict)
                ]).strip()
            elif isinstance(caption_obj, dict):
                text = str(caption_obj.get('text', '')).strip()
            elif 'text' in data and isinstance(data['text'], str):
                text = data['text'].strip()

            if user_id and text:
                comments.append({
                    'user_id': user_id,
                    'username': username,
                    'text': text,
                })

            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    comments.extend(self._extract_all_comments(v))

        elif isinstance(data, list):
            for item in data:
                comments.extend(self._extract_all_comments(item))

        return comments

    def _extract_all_ids(self, data):
        """Duyệt đệ quy gom sạch User ID / PK từ GraphQL/REST response."""
        found_ids = set()
        target_keys = (
            'id',
            'pk',
            'pk_id',
            'strong_id__',
            'user_id',
            'fbid',
            'node_id',
        )

        if isinstance(data, dict):
            for k, v in data.items():
                if k.lower() in target_keys and v:
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
        expected_text=None,
    ):
        """Kiểm tra danh sách user_list có nằm trong target_id (Follow, Like, Comment) hay không."""
        if not response_data or not isinstance(response_data, dict):
            return {
                'success': False,
                'type': check_type,
                'target_id': str(target_id),
                'message': (
                    'Không nhận được dữ liệu hoặc token/cookie đã hết hạn.'
                ),
                'results': [],
            }

        if 'errors' in response_data:
            err_msg = response_data.get('errors', [{}])[0].get(
                'message', 'GraphQL Query Error'
            )
            return {
                'success': False,
                'type': check_type,
                'target_id': str(target_id),
                'message': f'Lỗi GraphQL/Checkpoint: {err_msg}',
                'results': [],
            }

        target_id_str = str(target_id).strip()
        results = []

        if check_type.lower() == 'comment':
            comments = self._extract_all_comments(response_data)
            for uid in user_list:
                uid_str = str(uid).strip()
                user_comments = [
                    c['text'] for c in comments if c['user_id'] == uid_str
                ]
                is_commented = len(user_comments) > 0

                if not comments:
                    all_ids = self._extract_all_ids(response_data)
                    all_ids.discard(target_id_str)
                    is_commented = uid_str in all_ids

                text_matched = True
                if expected_text and is_commented and user_comments:
                    text_matched = any(
                        expected_text.lower() in t.lower() for t in user_comments
                    )

                is_active = (
                    (is_commented and text_matched)
                    if expected_text
                    else is_commented
                )
                results.append({
                    'user_id': uid_str,
                    'is_active': is_active,
                    'user_comments': user_comments,
                })
        else:
            all_ids = self._extract_all_ids(response_data)
            all_ids.discard(target_id_str)
            for uid in user_list:
                uid_str = str(uid).strip()
                is_exist = uid_str in all_ids
                results.append({'user_id': uid_str, 'is_active': is_exist})

        return {
            'success': True,
            'type': check_type,
            'target_id': target_id_str,
            'results': results,
            'message': (
                f'Đã kiểm tra danh sách người dùng cho target {target_id_str}.'
            ),
        }

    # ================= ĐA LUỒNG DUYỆT JOBS =================
    def _worker(
        self, target_id, user_list, action_type, delay_range, expected_text
    ):
        time.sleep(random.uniform(delay_range[0], delay_range[1]))
        if action_type == 'like':
            res_json = self.like(target_id)
        elif action_type == 'comment':
            res_json = self.comment(target_id)
        else:
            res_json = self.follow(target_id)

        return self.check_list(
            target_id=target_id,
            user_list=user_list,
            response_data=res_json,
            check_type=action_type,
            expected_text=expected_text,
        )

    def run_multi_threads(
        self,
        user_list,
        target_list,
        action_type='follow',
        max_threads=3,
        batch_size=20,
        delay_range=(1.5, 3.5),
        batch_cooldown=8,
        expected_text=None,
    ):
        total = len(target_list)
        all_results = []
        completed = 0

        safe_log(
            f'[*] Bắt đầu duyệt job [{action_type.upper()}] cho danh sách user.'
        )
        safe_log(
            f'[*] Tổng số target: {total} | Số luồng: {max_threads} | Kích'
            f' thước lô: {batch_size}\n'
        )

        for i in range(0, total, batch_size):
            batch = target_list[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total + batch_size - 1) // batch_size

            safe_log(
                f'--- ĐANG CHẠY LÔ {batch_num}/{total_batches} ({len(batch)}'
                ' Target) ---'
            )

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {
                    executor.submit(
                        self._worker,
                        target_id,
                        user_list,
                        action_type,
                        delay_range,
                        expected_text,
                    ): target_id
                    for target_id in batch
                }

                for future in as_completed(futures):
                    completed += 1
                    res = future.result()
                    all_results.append(res)
                    safe_log(
                        f'[{completed}/{total}] Target: {res["target_id"]} |'
                        f' Trạng thái kết quả: {res.get("success")}'
                    )

            if i + batch_size < total:
                safe_log(
                    f'[*] Nghỉ {batch_cooldown}s trước khi chuyển sang lô tiếp'
                    ' theo...\n'
                )
                time.sleep(batch_cooldown)

        return all_results
