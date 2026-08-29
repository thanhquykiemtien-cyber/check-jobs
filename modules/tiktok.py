class TikTok:
    def __init__(self, cookies=""):
        self.cookies = cookies

    def follow(self, target_id):
        return {}

    def like(self, target_id):
        return {}

    def comment(self, target_id):
        return {}

    def check_list(self, target_id, user_list, response_data=None, check_type="follow"):
        results = [
            {"user_id": str(u), "is_active": False, "comments_text": []}
            for u in user_list
        ]
        return {
            "success": True,
            "type": check_type,
            "target_id": str(target_id),
            "results": results,
            "message": "TikTok checker placeholder"
        }

# Alias để nếu import chữ thường cũng không lỗi
tiktok = TikTok
