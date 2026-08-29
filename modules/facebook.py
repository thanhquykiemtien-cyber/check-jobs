import requests
import re
import json
import base64
import time
import random
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

print_lock = Lock()

def safe_log(msg):
    with print_lock:
        print(msg)


class Facebook:
    def __init__(self, cookies):
        self.cookies = cookies
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'referer': 'https://www.facebook.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            'sec-ch-ua-full-version-list': '"Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
            'x-asbd-id': '359341',
            'x-fb-friendly-name': 'ProfileCometTopAppSectionQuery',
            'x-fb-lsd': 'dZIixoWHBBSmjDXX2WBt6I',
            'cookie': cookies,
        }

    # ================= GIỮ NGUYÊN GỐC 100% =================
    def data(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="147.0.7727.56", "Not.A/Brand";v="8.0.0.0", "Chromium";v="147.0.7727.56"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'viewport-width': '528',
            'cookie': self.cookies,
        }
        response = requests.get('https://www.facebook.com/', headers=headers).text
        avID = re.findall('"USER_ID":".*?"', response)[0].split('"USER_ID":"')[1].split('"')[0]
        dtsgID = re.findall('"dtsg":.*?,', response)[0].split('"token":"')[1].split('"')[0]
        return avID, dtsgID

    def follow(self, id):
        avID, dtsgID = self.data()
        self.headers['x-fb-friendly-name'] = 'ProfileCometTopAppSectionQuery'
        data = {
            'av': avID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometTopAppSectionQuery',
            'variables': '{"collectionToken":"YXBwX2NvbGxlY3Rpb246cGZiaWQwM3RGV1V4RDFxY1ZhTnp1RTdzZmNGcThxcE16blVVNEFjRnY0U3Rpa1NYR25NUEt4WE1lYzY5SlZFd1JYd1E0c0tNNXBMSzJyVGtXUG9FZ2N6ZVZkOWFlc0hGMkp2bA==","scale":3,"sectionToken":"YXBwX3NlY3Rpb246MTAwMDA3NTYxODA4MjA1OjIzNTYzMTgzNDk=","useDefaultActor":false,"userID":"'+ str(id) +'","__relay_internal__pv__FBProfile_enable_perf_improv_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoMediaContentContainer_comet_reels_video_footer_defer_loading_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoMediaContentContainer_comet_video_document_picture_in_picture_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoMediaContentContainer_enable_chapters_pill_gkrelayprovider":false,"__relay_internal__pv__ShouldEnableBakedInTextUnifiedVideorelayprovider":false,"__relay_internal__pv__FBUnifiedVideoCometVideoMedia_comet_photosensitive_content_warning_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoMediaHeaderControls_enable_chapters_pill_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoMediaFooter_organic_ad_cta_on_comet_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoMediaFooter_enable_meta_ai_pill_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoMediaFooter_enable_ai_embodiment_chat_pill_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoMediaFooter_enable_video_augment_pills_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoPlayerScrubber_fb_comet_vpv_heatmap_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoDescriptionWithEntities_comet_translations_revamp_sync_caption_with_audio_gkrelayprovider":false,"__relay_internal__pv__FBUnifiedVideoFeedbackBar_comet_reels_save_button_gkrelayprovider":false,"__relay_internal__pv__usePushPipEngagementCounts_comet_video_document_picture_in_picture_gkrelayprovider":false,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedVideoMenu_fb_reels_ranking_debug_tool_gkrelayprovider":false,"__relay_internal__pv__CometAudioLanguageUtils_comet_translations_revamp_preferred_languages_gkrelayprovider":false}',
            'doc_id': '37888031957506932',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            return response
        except Exception:
            return {}

    def like(self, id):
        avID, dtsgID = self.data()
        target = "feedback:" + id
        target_id = str(base64.b64encode(bytes(target, 'UTF-8'))).split("b'")[1].split("'")[0]
        self.headers['x-fb-friendly-name'] = 'CometUFIReactionsDialogTabContentRefetchQuery'
        data = {
            'av': avID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIReactionsDialogTabContentRefetchQuery',
            'variables': '{"count":10,"cursor":null,"feedbackTargetID":"'+ str(target_id) +'","reactionID":null,"scale":1,"id":"'+ str(target_id) +'"}',
            'doc_id': '37480094514909095',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            return response
        except Exception:
            return {}

    def comment(self, id):
        avID, dtsgID = self.data()
        target = "feedback:" + id
        target_id = str(base64.b64encode(bytes(target, 'UTF-8'))).split("b'")[1].split("'")[0]
        self.headers['x-fb-friendly-name'] = 'CommentListComponentsRootQuery'
        data = {
            'av': avID,
            'fb_dtsg': dtsgID,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
            'variables': '{"commentsIntentToken":"RANKED_UNFILTERED_CHRONOLOGICAL_REPLIES_INTENT_V1","feedLocation":"COMET_MEDIA_VIEWER","feedbackSource":65,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"'+ str(target_id) +'","__relay_internal__pv__CometUFICommentAutoTranslationTyperelayprovider":"AUTO_TRANSLATE","__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__CometUFICommentActionLinksRewriteEnabledrelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false}',
            'doc_id': '28454408110916047',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            return response
        except Exception:
            return {}

    # ================= CÁC HÀM XỬ LÝ & CHECK =================
    def _extract_all_ids(self, data):
        """Hàm quét đệ quy trích xuất toàn bộ user ID / profile ID có trong response."""
        found_ids = set()
        if isinstance(data, dict):
            for k, v in data.items():
                if k.lower() in ('id', 'actorid', 'userid', 'fbid', 'accountid', 'qeid') and v:
                    found_ids.add(str(v).strip())
                if isinstance(v, str) and ('qeid' in v or 'actorId' in v or '"id"' in v):
                    try:
                        json_str = v[1:] if v.startswith('J{') else v
                        nested_json = json.loads(json_str)
                        found_ids.update(self._extract_all_ids(nested_json))
                    except Exception:
                        pass
                else:
                    found_ids.update(self._extract_all_ids(v))
        elif isinstance(data, list):
            for item in data:
                found_ids.update(self._extract_all_ids(item))
        return found_ids

    def _extract_comments_by_user(self, response_data, my_id):
        """Trích xuất chính xác nội dung text comment của my_id."""
        user_comments = []
        my_id_str = str(my_id).strip()
        try:
            edges = response_data.get('data', {}).get('node', {}).get('comment_rendering_instance_for_feed_location', {}).get('comments', {}).get('edges', [])
            for edge in edges:
                node = edge.get('node', {})
                author_id = str(node.get('author', {}).get('id', '')).strip()
                if author_id == my_id_str:
                    comment_text = (
                        node.get('body', {}).get('text') or 
                        node.get('preferred_body', {}).get('text') or 
                        ""
                    )
                    user_comments.append(comment_text)
        except Exception:
            pass
        return user_comments

    def check_list(self, target_id, user_list, response_data, check_type="follow"):
        """Kiểm tra danh sách user_list có nằm trong target_id hay không."""
        if not response_data:
            return {
                "success": False,
                "type": check_type,
                "target_id": str(target_id),
                "message": "Không nhận được response hoặc request lỗi.",
                "results": []
            }

        all_ids_in_list = self._extract_all_ids(response_data)
        target_id_str = str(target_id).strip()
        results = []

        for uid in user_list:
            uid_str = str(uid).strip()
            is_exist = uid_str in all_ids_in_list

            comments_list = []
            if check_type == "comment" and is_exist:
                comments_list = self._extract_comments_by_user(response_data, uid_str)

            results.append({
                "user_id": uid_str,
                "is_active": is_exist,
                "comments_text": comments_list
            })

        return {
            "success": True,
            "type": check_type,
            "target_id": target_id_str,
            "results": results,
            "message": f"Đã kiểm tra danh sách người dùng cho target {target_id_str}."
        }

    # ================= ĐA LUỒNG DUYỆT JOBS =================
    def _worker(self, target_id, user_list, action_type, delay_range):
        """Xử lý theo đúng loại job (follow, like, comment)."""
        time.sleep(random.uniform(delay_range[0], delay_range[1]))
        
        if action_type == 'like':
            res_json = self.like(target_id)
        elif action_type == 'comment':
            res_json = self.comment(target_id)
        else:
            res_json = self.follow(target_id)

        return self.check_list(target_id=target_id, user_list=user_list, response_data=res_json, check_type=action_type)

    def run_multi_threads(self, user_list, target_list, action_type="follow", max_threads=3, batch_size=20, delay_range=(1.5, 3.5), batch_cooldown=8):
        """
        Quét đa luồng kiểm tra xem danh sách user_list đã thực hiện action_type trên danh sách target_list chưa.
        """
        total = len(target_list)
        all_results = []
        completed = 0

        safe_log(f"[*] Bắt đầu duyệt job [{action_type.upper()}] cho danh sách user.")
        safe_log(f"[*] Tổng số target: {total} | Số luồng: {max_threads} | Kích thước lô: {batch_size}\n")

        for i in range(0, total, batch_size):
            batch = target_list[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total + batch_size - 1) // batch_size

            safe_log(f"--- ĐANG CHẠY LÔ {batch_num}/{total_batches} ({len(batch)} Target) ---")

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {
                    executor.submit(self._worker, target_id, user_list, action_type, delay_range): target_id 
                    for target_id in batch
                }

                for future in as_completed(futures):
                    completed += 1
                    res = future.result()
                    all_results.append(res)
                    
                    safe_log(f"[{completed}/{total}] Target: {res['target_id']} | Trạng thái kết quả: {res.get('success')}")

            if i + batch_size < total:
                safe_log(f"[*] Nghỉ {batch_cooldown}s trước khi chuyển sang lô tiếp theo...\n")
                time.sleep(batch_cooldown)

        return all_results
