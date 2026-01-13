# 🌱 HabitBloom - 习惯养成花园

<p align="center">
  <img src="logo.png" alt="HabitBloom Logo" width="50"/>
</p>


<p align="center">
  <strong>让习惯如花般绽放</strong>
</p>

<p align="center">
  <a href="#功能特性">功能特性</a> •
  <a href="#系统要求">系统要求</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#项目结构">项目结构</a> •
  <a href="#技术栈">技术栈</a>
</p>

---

## 📱 应用简介

HabitBloom 是一款基于可视化花园的个人习惯养成应用。用户通过每日完成习惯来"浇灌"自己的习惯花园，每个习惯对应一种植物，完成情况直接影响植物的生长状态，形成正向的视觉激励。

## ✨ 功能特性

### 🌻 可视化激励系统
- 习惯进度以植物生长状态呈现
- 种子 → 发芽 → 幼苗 → 开花 → 结果
- 完成打卡即为植物"浇水"

### 📊 本地数据存储
- 所有数据存储在设备本地
- 无需网络，保护隐私
- 支持数据导出/导入

### 🎯 智能习惯管理
- 自定义习惯名称、图标、频率
- 四大分类：健康、学习、工作、生活
- 难度等级设置

### 🏆 成就系统
- 连续打卡里程碑（7天、21天、66天）
- 累计打卡成就
- 特殊成就徽章

### 📈 数据统计
- 月度完成率
- 连续打卡记录
- 习惯趋势分析

### 🔔 提醒系统
- 自定义提醒时间
- 每日定时提醒

## 📋 系统要求

- **Android 版本**: 8.0 (API 26) 及以上
- **存储空间**: 约 20MB
- **权限**: 通知权限（可选）

## 🚀 快速开始

### 编译构建

1. **克隆项目**
```bash
git clone https://github.com/pznger/HabitBloom.git
cd HabitBloom
```

2. **使用 Android Studio 打开项目**

3. **同步 Gradle**
```bash
./gradlew build
```

4. **构建 APK**
```bash
# Debug 版本
./gradlew assembleDebug

# Release 版本
./gradlew assembleRelease
```

APK 文件位置：`app/build/outputs/apk/`

### 安装运行

1. 连接 Android 设备或启动模拟器
2. 运行：
```bash
./gradlew installDebug
```

## 📁 项目结构

```
HabitBloom/
├── app/
│   ├── src/main/
│   │   ├── java/com/habitbloom/
│   │   │   ├── HabitBloomApplication.java    # Application 类
│   │   │   ├── data/                          # 数据层
│   │   │   │   ├── database/                  # Room 数据库
│   │   │   │   │   ├── AppDatabase.java       # 数据库类
│   │   │   │   │   ├── dao/                   # 数据访问对象
│   │   │   │   │   │   ├── UserDao.java
│   │   │   │   │   │   ├── HabitDao.java
│   │   │   │   │   │   ├── HabitRecordDao.java
│   │   │   │   │   │   ├── ReminderDao.java
│   │   │   │   │   │   ├── AchievementDao.java
│   │   │   │   │   │   └── GardenStateDao.java
│   │   │   │   │   └── entity/                # 实体类
│   │   │   │   │       ├── User.java
│   │   │   │   │       ├── Habit.java
│   │   │   │   │       ├── HabitRecord.java
│   │   │   │   │       ├── Reminder.java
│   │   │   │   │       ├── Achievement.java
│   │   │   │   │       └── GardenState.java
│   │   │   │   └── repository/                # 数据仓库
│   │   │   │       ├── HabitRepository.java
│   │   │   │       ├── AchievementRepository.java
│   │   │   │       └── UserRepository.java
│   │   │   ├── ui/                            # 表现层
│   │   │   │   ├── splash/                    # 启动页
│   │   │   │   │   └── SplashActivity.java
│   │   │   │   ├── main/                      # 主界面
│   │   │   │   │   └── MainActivity.java
│   │   │   │   ├── garden/                    # 花园模块
│   │   │   │   │   ├── GardenFragment.java
│   │   │   │   │   └── PlantCardAdapter.java
│   │   │   │   ├── habit/                     # 习惯模块
│   │   │   │   │   ├── HabitListFragment.java
│   │   │   │   │   ├── HabitDetailActivity.java
│   │   │   │   │   ├── CreateHabitActivity.java
│   │   │   │   │   └── HabitListAdapter.java
│   │   │   │   ├── stats/                     # 统计模块
│   │   │   │   │   ├── StatsFragment.java
│   │   │   │   │   └── AchievementAdapter.java
│   │   │   │   ├── settings/                  # 设置模块
│   │   │   │   │   └── SettingsFragment.java
│   │   │   │   └── viewmodel/                 # ViewModel
│   │   │   │       ├── HabitViewModel.java
│   │   │   │       ├── StatsViewModel.java
│   │   │   │       └── UserViewModel.java
│   │   │   ├── notification/                  # 通知模块
│   │   │   │   └── ReminderReceiver.java
│   │   │   └── utils/                         # 工具类
│   │   │       ├── DateUtils.java
│   │   │       └── Constants.java
│   │   └── res/                               # 资源文件
│   │       ├── layout/                        # 布局文件
│   │       ├── drawable/                      # 图形资源
│   │       ├── values/                        # 值资源
│   │       └── menu/                          # 菜单资源
│   └── build.gradle.kts                       # 模块构建配置
├── docs/                                      # 文档
│   ├── 需求规格说明书.md
│   └── 系统设计说明书.md
├── gradle/
│   └── libs.versions.toml                     # 依赖版本管理
├── build.gradle.kts                           # 项目构建配置
├── settings.gradle.kts                        # 项目设置
└── README.md                                  # 项目说明
```

## 🛠 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| **开发语言** | Java | Android 原生开发 |
| **最低版本** | Android 8.0 (API 26) | 兼容主流设备 |
| **架构模式** | MVVM | Model-View-ViewModel |
| **数据库** | Room | Android 官方 ORM |
| **异步处理** | LiveData + Executor | 响应式数据 |
| **UI 组件** | Material Design 3 | 现代化设计 |
| **构建工具** | Gradle Kotlin DSL | 构建自动化 |

## 📦 依赖库

```toml
# 核心依赖
androidx.appcompat = "1.6.1"
com.google.android.material = "1.10.0"
androidx.constraintlayout = "2.1.4"

# Room 数据库
androidx.room = "2.6.1"

# Lifecycle 组件
androidx.lifecycle = "2.6.2"

# Navigation 组件
androidx.navigation = "2.7.5"

# WorkManager
androidx.work = "2.9.0"

# Gson
com.google.code.gson = "2.10.1"
```

## 🎨 UI/UX 设计

### 色彩方案
- **主色调**: #4CAF50 (绿色 - 代表生长)
- **强调色**: #FF9800 (橙色 - 高亮提示)
- **背景色**: #F5F5F5 (浅灰 - 舒适阅读)

### 植物生长阶段
| 阶段 | 所需天数 | 图标 |
|------|----------|------|
| 种子 | 0天 | 🫘 |
| 发芽 | 3天 | 🌱 |
| 幼苗 | 7天 | 🌿 |
| 开花 | 21天 | 🌸 |
| 结果 | 66天 | 💐 |

## 📄 文档

- [需求规格说明书](docs/需求规格说明书.md)
- [系统设计说明书](docs/系统设计说明书.md)

## 🔐 隐私说明

- 所有数据存储在本地设备
- 不收集任何用户个人信息
- 不需要网络连接

## 📝 版本历史

### v1.0.0 (2026-01-13)
- 🎉 首次发布
- ✅ 习惯创建与管理
- ✅ 每日打卡功能
- ✅ 花园可视化系统
- ✅ 统计与成就系统
- ✅ 深色模式支持

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

<p align="center">
  <strong>🌱 让好习惯如花般绽放 🌸</strong>
</p>












# 附件：HabitBloom 系统设计说明书

## 1. 系统架构设计

### 1.1 总体架构图

![PlantUML diagram](D:\Android\androidworkspace\My Application\docs\总体架构图)

### 1.2 架构说明

#### 1.2.1 架构模式：MVVM (Model-View-ViewModel)

采用 Android 推荐的 MVVM 架构模式，实现关注点分离：

| 层级          | 职责                   | 组件                           |
| ------------- | ---------------------- | ------------------------------ |
| **View**      | 负责UI展示和用户交互   | Activity, Fragment, XML Layout |
| **ViewModel** | 负责UI逻辑和状态管理   | ViewModel + LiveData           |
| **Model**     | 负责数据存储和业务逻辑 | Repository, Room, Entity       |

#### 1.2.2 分层设计

**表现层 (Presentation Layer)**

- 包含所有 Activity 和 Fragment
- 通过 DataBinding 实现视图绑定
- 观察 ViewModel 中的 LiveData 更新UI

**ViewModel层**

- 持有 LiveData 状态数据
- 处理用户交互事件
- 调用 Repository 进行数据操作
- 生命周期感知，避免内存泄漏

**数据仓库层 (Repository Layer)**

- 统一数据访问接口
- 协调本地数据源
- 处理数据转换和业务逻辑

**数据层 (Data Layer)**

- Room 数据库持久化存储
- SharedPreferences 配置存储
- 文件系统用于数据导出/导入

### 1.3 技术选型

| 类别     | 技术方案                   | 说明             |
| -------- | -------------------------- | ---------------- |
| 开发语言 | Java                       | Android 原生开发 |
| 最低版本 | Android 8.0 (API 26)       | 兼容性考虑       |
| 数据库   | Room                       | Android 官方 ORM |
| 异步处理 | LiveData + Executor        | 响应式数据       |
| UI 组件  | Material Design 3          | 现代化设计       |
| 导航     | Navigation Component       | 统一导航管理     |
| 通知     | WorkManager + AlarmManager | 定时提醒         |

---

## 2. UI/UX 设计

### 2.1 页面导航结构

![PlantUML diagram](docs\导航结构)

### 2.2 页面原型设计

#### 2.2.1 启动页 (SplashActivity)

<img src="docs\启动页" alt="845690910f4cb18cb7f12f09973022c0" style="zoom:33%;" />

#### 2.2.2 主花园页面 (GardenFragment)

<img src="docs\主花园" alt="970c1608d9ebdf9126238e8a3c21e8ba" style="zoom:33%;" />

#### 2.2.3 习惯详情页 (HabitDetailActivity)

<img src="docs\习惯详情" alt="1ddd0e6da01e2d163d0b41236a043692" style="zoom: 33%;" />

#### 2.2.4 创建习惯页面 (CreateHabitActivity)

<img src="docs\创建习惯" alt="fdefeae958c8d940dcc98fc68ebdb9b0_720" style="zoom: 25%;" />

#### 2.2.5 统计页面 (StatsFragment)

<img src="docs\统计" alt="c3cb507e4f1ed02bd8a856d9cba1e8ce" style="zoom:33%;" />

#### 2.2.6 设置页面 (SettingsFragment)

<img src="docs\设置" alt="81da398d4a92f75759a7cc7d2c7ba4d0" style="zoom:33%;" />

### 2.3 设计规范

#### 2.3.1 色彩方案

| 用途     | 颜色代码 | 说明           |
| -------- | -------- | -------------- |
| 主色调   | #4CAF50  | 绿色，代表生长 |
| 主色调深 | #388E3C  | 深绿色         |
| 主色调浅 | #C8E6C9  | 浅绿色背景     |
| 强调色   | #FF9800  | 橙色，用于高亮 |
| 背景色   | #F5F5F5  | 浅灰背景       |
| 卡片色   | #FFFFFF  | 白色卡片       |
| 文字主色 | #212121  | 深灰文字       |
| 文字次色 | #757575  | 灰色文字       |
| 成功色   | #4CAF50  | 绿色           |
| 警告色   | #FFC107  | 黄色           |
| 错误色   | #F44336  | 红色           |

#### 2.3.2 字体规范

| 用途     | 字号 | 字重    |
| -------- | ---- | ------- |
| 大标题   | 24sp | Bold    |
| 标题     | 20sp | Medium  |
| 子标题   | 16sp | Medium  |
| 正文     | 14sp | Regular |
| 辅助文字 | 12sp | Regular |
| 按钮文字 | 14sp | Medium  |

#### 2.3.3 间距规范

| 用途     | 尺寸 |
| -------- | ---- |
| 页面边距 | 16dp |
| 卡片边距 | 12dp |
| 组件间距 | 8dp  |
| 小间距   | 4dp  |
| 圆角     | 12dp |

#### 2.3.4 动画规范

| 动画类型 | 时长  | 曲线        |
| -------- | ----- | ----------- |
| 页面过渡 | 300ms | ease-in-out |
| 植物生长 | 500ms | ease-out    |
| 浇水效果 | 200ms | ease-in     |
| 按钮反馈 | 100ms | linear      |
| 成就解锁 | 800ms | bounce      |

---

## 3. 数据库设计

### 3.1 ER图

![exported_image](docs\er)

### 3.2 表结构设计

#### 3.2.1 users 表 - 用户信息表

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL DEFAULT '用户',
    avatar_color TEXT DEFAULT '#4CAF50',
    daily_goal_time TEXT DEFAULT '08:00',
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
    last_login INTEGER
);
```

| 字段            | 类型    | 约束     | 说明         |
| --------------- | ------- | -------- | ------------ |
| user_id         | INTEGER | PK, AUTO | 用户唯一标识 |
| username        | TEXT    | NOT NULL | 用户昵称     |
| avatar_color    | TEXT    | DEFAULT  | 头像颜色     |
| daily_goal_time | TEXT    | DEFAULT  | 每日目标时段 |
| created_at      | INTEGER | NOT NULL | 创建时间戳   |
| last_login      | INTEGER | NULL     | 最后登录时间 |

#### 3.2.2 habits 表 - 习惯信息表

```sql
CREATE TABLE habits (
    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    category TEXT CHECK(category IN ('health', 'study', 'work', 'life')) DEFAULT 'life',
    icon TEXT DEFAULT '🌱',
    plant_type TEXT CHECK(plant_type IN ('flower', 'tree', 'cactus', 'herb')) DEFAULT 'flower',
    target_frequency INTEGER DEFAULT 7,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_completed INTEGER DEFAULT 0,
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5) DEFAULT 3,
    is_active INTEGER DEFAULT 1,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_habits_user_id ON habits(user_id);
CREATE INDEX idx_habits_category ON habits(category);
```

| 字段             | 类型    | 约束         | 说明                         |
| ---------------- | ------- | ------------ | ---------------------------- |
| habit_id         | INTEGER | PK, AUTO     | 习惯唯一标识                 |
| user_id          | INTEGER | FK, NOT NULL | 关联用户                     |
| name             | TEXT    | NOT NULL     | 习惯名称                     |
| category         | TEXT    | CHECK        | 分类(health/study/work/life) |
| icon             | TEXT    | DEFAULT      | 图标emoji                    |
| plant_type       | TEXT    | CHECK        | 植物类型                     |
| target_frequency | INTEGER | DEFAULT 7    | 每周目标次数                 |
| current_streak   | INTEGER | DEFAULT 0    | 当前连续天数                 |
| longest_streak   | INTEGER | DEFAULT 0    | 最长连续天数                 |
| total_completed  | INTEGER | DEFAULT 0    | 总完成次数                   |
| difficulty       | INTEGER | CHECK 1-5    | 难度等级                     |
| is_active        | INTEGER | DEFAULT 1    | 是否启用                     |
| created_at       | INTEGER | NOT NULL     | 创建时间戳                   |

#### 3.2.3 habit_records 表 - 打卡记录表

```sql
CREATE TABLE habit_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    record_date TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_time TEXT,
    notes TEXT,
    plant_growth_stage INTEGER DEFAULT 0,
    UNIQUE(habit_id, record_date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);

CREATE INDEX idx_records_habit_id ON habit_records(habit_id);
CREATE INDEX idx_records_date ON habit_records(record_date);
```

| 字段               | 类型    | 约束         | 说明                 |
| ------------------ | ------- | ------------ | -------------------- |
| record_id          | INTEGER | PK, AUTO     | 记录唯一标识         |
| habit_id           | INTEGER | FK, NOT NULL | 关联习惯             |
| record_date        | TEXT    | NOT NULL     | 记录日期(yyyy-MM-dd) |
| completed          | INTEGER | DEFAULT 0    | 是否完成(0/1)        |
| completed_time     | TEXT    | NULL         | 完成时间(HH:mm)      |
| notes              | TEXT    | NULL         | 备注/日记            |
| plant_growth_stage | INTEGER | DEFAULT 0    | 植物生长阶段         |

#### 3.2.4 reminders 表 - 提醒设置表

```sql
CREATE TABLE reminders (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    reminder_time TEXT NOT NULL,
    days_of_week TEXT DEFAULT '1,2,3,4,5,6,7',
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);

CREATE INDEX idx_reminders_habit_id ON reminders(habit_id);
```

| 字段          | 类型    | 约束         | 说明                  |
| ------------- | ------- | ------------ | --------------------- |
| reminder_id   | INTEGER | PK, AUTO     | 提醒唯一标识          |
| habit_id      | INTEGER | FK, NOT NULL | 关联习惯              |
| reminder_time | TEXT    | NOT NULL     | 提醒时间(HH:mm)       |
| days_of_week  | TEXT    | DEFAULT      | 周几提醒(1-7逗号分隔) |
| is_active     | INTEGER | DEFAULT 1    | 是否启用              |

#### 3.2.5 achievements 表 - 成就表

```sql
CREATE TABLE achievements (
    achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 1,
    achievement_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    badge_icon TEXT NOT NULL,
    unlocked_at INTEGER,
    requirement_value INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_achievements_user_id ON achievements(user_id);
```

| 字段              | 类型    | 约束         | 说明                  |
| ----------------- | ------- | ------------ | --------------------- |
| achievement_id    | INTEGER | PK, AUTO     | 成就唯一标识          |
| user_id           | INTEGER | FK, NOT NULL | 关联用户              |
| achievement_type  | TEXT    | NOT NULL     | 成就类型              |
| title             | TEXT    | NOT NULL     | 成就标题              |
| description       | TEXT    | NULL         | 成就描述              |
| badge_icon        | TEXT    | NOT NULL     | 徽章图标              |
| unlocked_at       | INTEGER | NULL         | 解锁时间(null=未解锁) |
| requirement_value | INTEGER | NULL         | 达成条件值            |

#### 3.2.6 garden_states 表 - 花园状态表

```sql
CREATE TABLE garden_states (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 1,
    habit_id INTEGER NOT NULL,
    plant_growth INTEGER DEFAULT 0,
    plant_health INTEGER DEFAULT 100,
    last_watered TEXT,
    stage INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);

CREATE INDEX idx_garden_user_id ON garden_states(user_id);
CREATE INDEX idx_garden_habit_id ON garden_states(habit_id);
```

| 字段         | 类型    | 约束         | 说明            |
| ------------ | ------- | ------------ | --------------- |
| state_id     | INTEGER | PK, AUTO     | 状态唯一标识    |
| user_id      | INTEGER | FK, NOT NULL | 关联用户        |
| habit_id     | INTEGER | FK, NOT NULL | 关联习惯        |
| plant_growth | INTEGER | DEFAULT 0    | 生长进度(0-100) |
| plant_health | INTEGER | DEFAULT 100  | 健康度(0-100)   |
| last_watered | TEXT    | NULL         | 最后浇水日期    |
| stage        | INTEGER | DEFAULT 1    | 生长阶段(1-5)   |

---

## 4. 模块设计

### 4.1 包结构

```
com.habitbloom
├── HabitBloomApplication.java       # Application类
├── ui/                              # UI层
│   ├── splash/                      # 启动页
│   │   └── SplashActivity.java
│   ├── main/                        # 主页面
│   │   ├── MainActivity.java
│   │   └── MainViewModel.java
│   ├── garden/                      # 花园模块
│   │   ├── GardenFragment.java
│   │   ├── GardenViewModel.java
│   │   └── PlantCardAdapter.java
│   ├── habit/                       # 习惯模块
│   │   ├── HabitListFragment.java
│   │   ├── HabitDetailActivity.java
│   │   ├── CreateHabitActivity.java
│   │   ├── HabitViewModel.java
│   │   └── HabitAdapter.java
│   ├── stats/                       # 统计模块
│   │   ├── StatsFragment.java
│   │   ├── StatsViewModel.java
│   │   └── AchievementAdapter.java
│   └── settings/                    # 设置模块
│       ├── SettingsFragment.java
│       └── SettingsViewModel.java
├── data/                            # 数据层
│   ├── database/                    # 数据库
│   │   ├── AppDatabase.java
│   │   ├── entity/                  # 实体类
│   │   │   ├── User.java
│   │   │   ├── Habit.java
│   │   │   ├── HabitRecord.java
│   │   │   ├── Reminder.java
│   │   │   ├── Achievement.java
│   │   │   └── GardenState.java
│   │   └── dao/                     # 数据访问
│   │       ├── UserDao.java
│   │       ├── HabitDao.java
│   │       ├── HabitRecordDao.java
│   │       ├── ReminderDao.java
│   │       ├── AchievementDao.java
│   │       └── GardenStateDao.java
│   ├── repository/                  # 数据仓库
│   │   ├── HabitRepository.java
│   │   ├── RecordRepository.java
│   │   ├── AchievementRepository.java
│   │   └── UserRepository.java
│   └── model/                       # 数据模型
│       ├── HabitWithRecords.java
│       └── StatsData.java
├── notification/                    # 通知模块
│   ├── ReminderManager.java
│   ├── ReminderReceiver.java
│   └── NotificationHelper.java
├── utils/                           # 工具类
│   ├── DateUtils.java
│   ├── PlantUtils.java
│   ├── ExportUtils.java
│   └── Constants.java
└── widget/                          # 自定义控件
    ├── PlantView.java
    ├── ProgressCircleView.java
    └── CalendarView.java
```

### 4.2 核心类设计

#### 4.2.1 HabitRepository - 习惯数据仓库

```java
public class HabitRepository {
    private final HabitDao habitDao;
    private final HabitRecordDao recordDao;
    private final GardenStateDao gardenDao;
    private final ExecutorService executor;

    // 获取所有活跃习惯
    public LiveData<List<Habit>> getAllActiveHabits();
    
    // 创建习惯
    public void createHabit(Habit habit, Callback callback);
    
    // 打卡
    public void checkIn(long habitId, String notes, Callback callback);
    
    // 获取习惯详情
    public LiveData<HabitWithRecords> getHabitWithRecords(long habitId);
    
    // 更新连续天数
    private void updateStreak(long habitId);
    
    // 更新植物状态
    private void updatePlantGrowth(long habitId, int streak);
}
```

### 4.3 关键流程设计

#### 4.3.1 打卡流程时序图

![PlantUML diagram](D:\Android\androidworkspace\My Application\docs\时序图)

---

## 5. 安全设计

### 5.1 数据安全

- 所有数据存储在本地，不上传至服务器
- 导出数据使用 JSON 格式，便于用户备份
- 数据库使用 SQLite，无需额外加密

### 5.2 权限说明

| 权限                   | 用途             |
| ---------------------- | ---------------- |
| RECEIVE_BOOT_COMPLETED | 开机启动提醒服务 |
| SCHEDULE_EXACT_ALARM   | 精确定时提醒     |
| POST_NOTIFICATIONS     | 发送通知         |
| WRITE_EXTERNAL_STORAGE | 导出数据文件     |
| READ_EXTERNAL_STORAGE  | 导入数据文件     |
| VIBRATE                | 震动反馈         |

---

## 6. 版本历史

| 版本 | 日期       | 说明     |
| ---- | ---------- | -------- |
| 1.0  | 2026-01-13 | 初始版本 |
