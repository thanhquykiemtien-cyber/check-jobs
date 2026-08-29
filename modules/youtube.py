from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from googleapiclient.discovery import build

API_KEY = "AIzaSyCSmwl0zf-wB1SOFj3Gq5o4RIoMK7l7wYs"
print_lock = threading.Lock()


def safe_print(msg):
  with print_lock:
    print(msg)


class YouTube:

  def __init__(self, api_key: str = API_KEY):
    self.api_key = api_key
    self.client = build("youtube", "v3", developerKey=self.api_key)

  def is_subscribed_by_channel_id(
      self, user_channel_id: str, target_channel_id: str
  ) -> bool:
    """Kiểm tra Channel A (user_channel_id) có đăng ký Channel B (target_channel_id) hay không.

    Lưu ý: Chỉ kiểm tra được nếu Channel A để danh sách đăng ký ở chế độ CÔNG
    KHAI.
    """
    try:
      req = self.client.subscriptions().list(
          part="snippet",
          channelId=user_channel_id.strip(),
          forChannelId=target_channel_id.strip(),
      )
      res = req.execute()
      items = res.get("items", [])
      return len(items) > 0
    except Exception as e:
      safe_print(f"⚠️ Lỗi YouTube API cho [{user_channel_id}]: {e}")
      return False

  def check_list(
      self,
      target_channel_id: str,
      user_channel_list: list,
      check_type: str = "subscribe",
      max_threads: int = 3,
      batch_size: int = 20,
  ) -> dict:
    """Quét đa luồng kiểm tra danh sách user_channel_list đã subscribe target_channel_id chưa."""
    total = len(user_channel_list)
    results = []
    completed = 0

    safe_print(
        f"[*] Bắt đầu kiểm tra YouTube cho Target Channel ID:"
        f" {target_channel_id}"
    )

    for i in range(0, total, batch_size):
      batch = user_channel_list[i : i + batch_size]

      with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(
                self.is_subscribed_by_channel_id, user_id, target_channel_id
            ): user_id
            for user_id in batch
        }

        for future in as_completed(futures):
          user_id = futures[future]
          completed += 1
          try:
            is_sub = future.result()
          except Exception:
            is_sub = False

          results.append({
              "user_id": str(user_id),
              "is_active": is_sub,
              "comments_text": [],
          })
          safe_print(
              f"[{completed}/{total}] YouTube User: {user_id} | Kết quả:"
              f" {is_sub}"
          )

    return {
        "success": True,
        "type": check_type,
        "target_id": str(target_channel_id),
        "results": results,
        "message": (
            f"Đã kiểm tra đăng ký kênh cho target {target_channel_id} thành"
            " công."
        ),
    }