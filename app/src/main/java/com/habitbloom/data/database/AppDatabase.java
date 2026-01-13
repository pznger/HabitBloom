package com.habitbloom.data.database;

import android.content.Context;

import androidx.annotation.NonNull;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.sqlite.db.SupportSQLiteDatabase;

import com.habitbloom.data.database.dao.AchievementDao;
import com.habitbloom.data.database.dao.GardenStateDao;
import com.habitbloom.data.database.dao.HabitDao;
import com.habitbloom.data.database.dao.HabitRecordDao;
import com.habitbloom.data.database.dao.ReminderDao;
import com.habitbloom.data.database.dao.UserDao;
import com.habitbloom.data.database.entity.Achievement;
import com.habitbloom.data.database.entity.GardenState;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.data.database.entity.Reminder;
import com.habitbloom.data.database.entity.User;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Database(
        entities = {
                User.class,
                Habit.class,
                HabitRecord.class,
                Reminder.class,
                Achievement.class,
                GardenState.class
        },
        version = 1,
        exportSchema = false
)
public abstract class AppDatabase extends RoomDatabase {

    private static volatile AppDatabase INSTANCE;
    private static final int NUMBER_OF_THREADS = 4;
    public static final ExecutorService databaseExecutor = Executors.newFixedThreadPool(NUMBER_OF_THREADS);

    public abstract UserDao userDao();
    public abstract HabitDao habitDao();
    public abstract HabitRecordDao habitRecordDao();
    public abstract ReminderDao reminderDao();
    public abstract AchievementDao achievementDao();
    public abstract GardenStateDao gardenStateDao();

    public static AppDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                                    context.getApplicationContext(),
                                    AppDatabase.class,
                                    "habitbloom_database"
                            )
                            .addCallback(sRoomDatabaseCallback)
                            .build();
                }
            }
        }
        return INSTANCE;
    }

    private static final RoomDatabase.Callback sRoomDatabaseCallback = new RoomDatabase.Callback() {
        @Override
        public void onCreate(@NonNull SupportSQLiteDatabase db) {
            super.onCreate(db);
            // 初始化默认数据
            databaseExecutor.execute(() -> {
                // 创建默认用户
                UserDao userDao = INSTANCE.userDao();
                User defaultUser = new User();
                defaultUser.setUsername("用户");
                defaultUser.setAvatarColor("#4CAF50");
                defaultUser.setCreatedAt(System.currentTimeMillis());
                userDao.insert(defaultUser);

                // 创建默认成就
                AchievementDao achievementDao = INSTANCE.achievementDao();
                initializeAchievements(achievementDao);
            });
        }
    };

    private static void initializeAchievements(AchievementDao achievementDao) {
        // 连续打卡成就
        Achievement streak7 = new Achievement();
        streak7.setUserId(1);
        streak7.setAchievementType(Achievement.TYPE_STREAK_7);
        streak7.setTitle("初出茅庐");
        streak7.setDescription("连续打卡7天");
        streak7.setBadgeIcon("🌟");
        streak7.setRequirementValue(7);
        achievementDao.insert(streak7);

        Achievement streak21 = new Achievement();
        streak21.setUserId(1);
        streak21.setAchievementType(Achievement.TYPE_STREAK_21);
        streak21.setTitle("习惯养成者");
        streak21.setDescription("连续打卡21天");
        streak21.setBadgeIcon("🏆");
        streak21.setRequirementValue(21);
        achievementDao.insert(streak21);

        Achievement streak66 = new Achievement();
        streak66.setUserId(1);
        streak66.setAchievementType(Achievement.TYPE_STREAK_66);
        streak66.setTitle("习惯大师");
        streak66.setDescription("连续打卡66天");
        streak66.setBadgeIcon("👑");
        streak66.setRequirementValue(66);
        achievementDao.insert(streak66);

        // 累计打卡成就
        Achievement total10 = new Achievement();
        total10.setUserId(1);
        total10.setAchievementType(Achievement.TYPE_TOTAL_10);
        total10.setTitle("坚持不懈");
        total10.setDescription("累计打卡10次");
        total10.setBadgeIcon("💪");
        total10.setRequirementValue(10);
        achievementDao.insert(total10);

        Achievement total50 = new Achievement();
        total50.setUserId(1);
        total50.setAchievementType(Achievement.TYPE_TOTAL_50);
        total50.setTitle("持之以恒");
        total50.setDescription("累计打卡50次");
        total50.setBadgeIcon("🎯");
        total50.setRequirementValue(50);
        achievementDao.insert(total50);

        Achievement total100 = new Achievement();
        total100.setUserId(1);
        total100.setAchievementType(Achievement.TYPE_TOTAL_100);
        total100.setTitle("百战百胜");
        total100.setDescription("累计打卡100次");
        total100.setBadgeIcon("💎");
        total100.setRequirementValue(100);
        achievementDao.insert(total100);

        // 特殊成就
        Achievement perfectWeek = new Achievement();
        perfectWeek.setUserId(1);
        perfectWeek.setAchievementType(Achievement.TYPE_PERFECT_WEEK);
        perfectWeek.setTitle("完美一周");
        perfectWeek.setDescription("一周内所有习惯全部完成");
        perfectWeek.setBadgeIcon("🌈");
        perfectWeek.setRequirementValue(7);
        achievementDao.insert(perfectWeek);

        Achievement firstHabit = new Achievement();
        firstHabit.setUserId(1);
        firstHabit.setAchievementType(Achievement.TYPE_FIRST_HABIT);
        firstHabit.setTitle("种下第一颗种子");
        firstHabit.setDescription("创建第一个习惯");
        firstHabit.setBadgeIcon("🌱");
        firstHabit.setRequirementValue(1);
        achievementDao.insert(firstHabit);

        Achievement habitMaster = new Achievement();
        habitMaster.setUserId(1);
        habitMaster.setAchievementType(Achievement.TYPE_HABIT_MASTER);
        habitMaster.setTitle("花园主人");
        habitMaster.setDescription("同时培养5个习惯");
        habitMaster.setBadgeIcon("🏡");
        habitMaster.setRequirementValue(5);
        achievementDao.insert(habitMaster);
    }
}
