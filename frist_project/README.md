專案根目錄/
├── Controllers/           // 控制器，處理前端請求
│     └── TaskController.cs
│     └── RegistrationController.cs
│
├── Models/                // 資料模型
│     └── Task.cs
│     └── Registration.cs
│
├── Views/                 // 前端頁面
│     ├── Tasks/
│     │     └── Index.cshtml
│     │     └── Create.cshtml
│     │     └── Details.cshtml
│     └── Registrations/
│           └── Index.cshtml
│           └── Details.cshtml
│
├── wwwroot/               // 靜態資源（CSS, JS, 圖片）
│     ├── css/
│     ├── js/
│     └── images/
│
├── appsettings.json       // 專案設定檔
├── Program.cs             // 程式入口
├── Startup.cs             // 設定 ASP.NET 啟動設定
│
├── workingmap/            // 專案規劃與設計文件
│     ├── codemap/         // 程式架構、檔案地圖
│     └── workingflow/     // 流程圖、功能流程
│
└── README.md              // 專案說明文件