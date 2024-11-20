# 113-1 資料庫管理 - I'm in 專案範例

## 專案簡介

在學習過程中，常常會遇到作業難以完成或期中考前需要密集討論的情況。然而，找到適合的學習夥伴卻不容易。如果你有這些困擾，不用擔心！快來使用 **I'm in** 平台，找到你的最佳學習夥伴吧！

**I'm in** 提供一個給大學生發起讀書會的平台。主要目標是幫助大學生解決修課時難以及時討論課程問題的窘境。我們提供一種特殊形式的學習活動 - 「一次性讀書會」，讓大家能在特定日期和時段內租借教室，舉辦一次性的讀書會。

:link: **[展示影片連結](https://youtu.be/YG6_KMKiZ4s)**



## 使用者功能

### User （一般使用者）

#### 使用者登入、註冊

- 註冊：使用者可以註冊帳號設定使用者名稱、密碼及電子郵件信箱，系統會分配一個 user_id 給每位使用者。
- 登入：使用系統分配的 user_id 登入並驗證密碼。

#### 開設讀書會

- 使用者可以透過平台發起讀書會，設定讀書會內容、對應課程、參與人數上限等資訊，並選擇可用的教室及日期時段。

#### 列出所有可加入的讀書會

- 使用者可以透過此功能了解還沒額滿的讀書會資訊。

#### 參與／退出讀書會

- 使用者可以參加其他人發起的讀書會，從平台上選擇感興趣的讀書會加入；也可以退出已加入的讀書會。

#### 查詢活動紀錄

- 使用者可以查看自己曾經參與過的讀書會資訊。

#### 查詢課程

- 使用者可以透過關鍵字查詢指定教授或課程名稱的課程資訊。

#### 查詢指定日期下教室已被預約的時段

- 使用者可以透過日期查詢已被預約的教室及對應時段。

#### 修改使用者資訊

- 使用者可以修改自己的使用者名稱、密碼及電子郵件信箱。

### Admin （管理員／業務經營者）

除了上述 User 擁有的功能以外，還增加以下功能：

#### 管理功能

- 管理員可以 新增／移除／修改／查詢課程及教室。查詢功能可針對任一或數個項目進行關鍵字查詢。
- 提供管理員批次匯入課程資訊的功能 (`./action/course_management/UploadCourses`)。該功能可允許管理員上傳包含課程資訊的 CSV 檔，系統則會將檔案內的每一筆課程分別寫入資料庫。

#### 查詢／修改任一使用者資訊

- 管理員可以查看或修改任何使用者的資訊。

#### 查詢讀書會資訊

- 管理員可查詢這些讀書會的詳細資訊。



## 使用方法

- 預設連線通道為 **127.0.0.1:8800**，可至 `server.py` 及 `client.py` 修改
- 在 `DB_utils.py` 設定**資料庫名稱** (DB_NAME)、**使用者名稱** (DB_USER)、**主機位置** (DB_HOST)及**通訊埠** (DB_PORT)

先執行 `server.py` 啟動伺服器：

```bash
python .\server.py 
```

再透過 `client.py` 向伺服器連線：

```bash
python .\client.py 
```



## 技術細節

- 使用 Socket 建立 client-server 連線，搭配 Multithreading 達成多人同時連線

- 資料庫使用 PostgreSQL，使用套件 Psycopg2 對資料庫進行操作

- **交易管理**：針對 Admin 的【批次匯入課程資訊】的功能，為實現交易管理，在寫入的過程中如果
  出現違反資料表限制的情況，新增的動作會立即停止，而系統將 ROLLBACK 回滾該次交易，取消之前的所有資料庫異動。反之若匯入過程順利完成，系統將在最後 COMMIT 提交交易，確保所有的課程資訊都已成
  功儲存至資料庫。

  - 可參考 `./DB_util.py` 中的 `upload_courses()` 與 `./action/course_management/UploadCourses.py`。

- **併行控制**：針對【開設讀書會】功能，為避免不同使用者同時預約某教室的相同時段，造成資料衝突，在使用者輸入讀書會資訊並按下確認鍵後，系統會針對此功能加鎖，檢查該是否已被借用，若無則成功新增借用記錄到STUDY_EVENT_PERIOD 並且解鎖，若有則解鎖並回傳錯誤訊息，以確保教室不會被重複借用。

  - 可參考 `./DB_util.py` 中的 `create_study_group()`。

  

## 程式說明

1. **`./server.py`**
   - 包含伺服器端的主要功能。
   - 在連接資料庫後，透過 socket 建立監聽服務，接收來自客戶端的連線請求。
   - 每當接收到一個客戶端連線，會啟動一個獨立的執行緒（thread）處理該連線，確保伺服器能並行處理多個客戶端。
2. **`./client.py`**
   - 包含客戶端的主要功能。
   - 持續從伺服器接收訊息並顯示於終端機。
   - 當訊息包含特定標籤（tag）時，根據標籤執行對應的操作，例如讀取使用者輸入、解析 CSV 檔案、關閉 socket 連線並結束程式。
3. **`./DB_utils.py`**
   - 封裝與資料庫相關的功能，包含資料庫連線管理與查詢操作。
4. **`./action` 資料夾**
   - 每項執行動作被實作為一個類別，繼承抽象類別 `Action`，並實作其核心方法 `exec()`。
   - 此架構讓程式具備高度擴展性，開發者可透過新增 action 類別輕鬆增加新功能。
5. **`./role` 資料夾**
   - 為支援未來擴展更多角色類型（如 User 和 Admin 之外的角色），將角色實作為類別，並繼承基底類別 `Role`。
   - 每個角色類別共享基底類別的通用功能，並可擴展定義角色特有的行為與權限。



## 開發環境

- Windows 11

- Python: 3.10.9

  - psycopg2: 2.9.10
  - pandas: 2.2.2
  - tabulate: 0.9.0

- PostgreSQL: 16.4

  

## 參考資料

- README 說明文件及報告內容來自 **113-1資料庫管理**

