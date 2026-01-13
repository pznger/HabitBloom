package com.habitbloom.utils;

public class Constants {
    // 习惯分类
    public static final String CATEGORY_HEALTH = "health";
    public static final String CATEGORY_STUDY = "study";
    public static final String CATEGORY_WORK = "work";
    public static final String CATEGORY_LIFE = "life";

    // 植物类型
    public static final String PLANT_FLOWER = "flower";
    public static final String PLANT_TREE = "tree";
    public static final String PLANT_CACTUS = "cactus";
    public static final String PLANT_HERB = "herb";

    // 生长阶段
    public static final int STAGE_SEED = 1;
    public static final int STAGE_SPROUT = 2;
    public static final int STAGE_SEEDLING = 3;
    public static final int STAGE_FLOWERING = 4;
    public static final int STAGE_FRUIT = 5;

    // 生长阶段所需天数
    public static final int DAYS_TO_SPROUT = 3;
    public static final int DAYS_TO_SEEDLING = 7;
    public static final int DAYS_TO_FLOWERING = 21;
    public static final int DAYS_TO_FRUIT = 66;

    // 通知
    public static final String CHANNEL_ID_REMINDER = "habit_reminder";
    public static final String CHANNEL_NAME_REMINDER = "习惯提醒";
    public static final int NOTIFICATION_ID_REMINDER = 1001;

    // SharedPreferences
    public static final String PREF_NAME = "habitbloom_prefs";
    public static final String PREF_FIRST_LAUNCH = "first_launch";
    public static final String PREF_DARK_MODE = "dark_mode";
    public static final String PREF_GARDEN_THEME = "garden_theme";
    public static final String PREF_NOTIFICATION_ENABLED = "notification_enabled";

    // Intent extras
    public static final String EXTRA_HABIT_ID = "habit_id";
    public static final String EXTRA_FROM_NOTIFICATION = "from_notification";

    // Request codes
    public static final int REQUEST_CREATE_HABIT = 1001;
    public static final int REQUEST_EDIT_HABIT = 1002;
    public static final int REQUEST_NOTIFICATION_PERMISSION = 1003;

    // Animation durations
    public static final int ANIM_DURATION_SHORT = 200;
    public static final int ANIM_DURATION_MEDIUM = 300;
    public static final int ANIM_DURATION_LONG = 500;

    // 默认图标
    public static final String[] CATEGORY_ICONS = {
            "💪", "📖", "💼", "🏠"
    };

    public static final String[] PLANT_ICONS = {
            "🌸", "🌳", "🌵", "🌿"
    };

    public static final String[] HABIT_ICONS = {
            "🏃", "📚", "💧", "🧘", "✍️", "🎯", "💪", "🌅",
            "🎨", "🎸", "🍎", "😴", "🚶", "🧠", "💰", "🏋️"
    };

    public static String getCategoryIcon(String category) {
        switch (category) {
            case CATEGORY_HEALTH: return "💪";
            case CATEGORY_STUDY: return "📖";
            case CATEGORY_WORK: return "💼";
            case CATEGORY_LIFE: return "🏠";
            default: return "🌱";
        }
    }

    public static String getPlantIcon(String plantType, int stage) {
        switch (plantType) {
            case PLANT_FLOWER:
                switch (stage) {
                    case STAGE_SEED: return "🫘";
                    case STAGE_SPROUT: return "🌱";
                    case STAGE_SEEDLING: return "🌿";
                    case STAGE_FLOWERING: return "🌸";
                    case STAGE_FRUIT: return "💐";
                    default: return "🌱";
                }
            case PLANT_TREE:
                switch (stage) {
                    case STAGE_SEED: return "🫘";
                    case STAGE_SPROUT: return "🌱";
                    case STAGE_SEEDLING: return "🪴";
                    case STAGE_FLOWERING: return "🌲";
                    case STAGE_FRUIT: return "🌳";
                    default: return "🌱";
                }
            case PLANT_CACTUS:
                switch (stage) {
                    case STAGE_SEED: return "🫘";
                    case STAGE_SPROUT: return "🌱";
                    case STAGE_SEEDLING: return "🪴";
                    case STAGE_FLOWERING: return "🌵";
                    case STAGE_FRUIT: return "🏜️";
                    default: return "🌱";
                }
            case PLANT_HERB:
                switch (stage) {
                    case STAGE_SEED: return "🫘";
                    case STAGE_SPROUT: return "🌱";
                    case STAGE_SEEDLING: return "🌿";
                    case STAGE_FLOWERING: return "🍀";
                    case STAGE_FRUIT: return "🌾";
                    default: return "🌱";
                }
            default:
                return "🌱";
        }
    }

    public static String getStageName(int stage) {
        switch (stage) {
            case STAGE_SEED: return "种子";
            case STAGE_SPROUT: return "发芽";
            case STAGE_SEEDLING: return "幼苗";
            case STAGE_FLOWERING: return "开花";
            case STAGE_FRUIT: return "结果";
            default: return "种子";
        }
    }

    public static String getCategoryName(String category) {
        switch (category) {
            case CATEGORY_HEALTH: return "健康";
            case CATEGORY_STUDY: return "学习";
            case CATEGORY_WORK: return "工作";
            case CATEGORY_LIFE: return "生活";
            default: return "其他";
        }
    }

    public static String getPlantTypeName(String plantType) {
        switch (plantType) {
            case PLANT_FLOWER: return "花朵";
            case PLANT_TREE: return "树木";
            case PLANT_CACTUS: return "仙人掌";
            case PLANT_HERB: return "草本";
            default: return "植物";
        }
    }
}
