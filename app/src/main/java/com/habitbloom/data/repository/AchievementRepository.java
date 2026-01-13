package com.habitbloom.data.repository;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.dao.AchievementDao;
import com.habitbloom.data.database.dao.HabitDao;
import com.habitbloom.data.database.entity.Achievement;

import java.util.ArrayList;
import java.util.List;

public class AchievementRepository {
    private final AchievementDao achievementDao;
    private final HabitDao habitDao;

    public AchievementRepository(Application application) {
        AppDatabase db = AppDatabase.getDatabase(application);
        achievementDao = db.achievementDao();
        habitDao = db.habitDao();
    }

    public LiveData<List<Achievement>> getAllAchievements() {
        return achievementDao.getAchievementsByUser(1);
    }

    public LiveData<List<Achievement>> getUnlockedAchievements() {
        return achievementDao.getUnlockedAchievements(1);
    }

    public List<Achievement> getUnlockedAchievementsSync() {
        return achievementDao.getUnlockedAchievementsSync(1);
    }

    public int getUnlockedCount() {
        return achievementDao.getUnlockedCount(1);
    }

    public int getTotalCount() {
        return achievementDao.getTotalCount(1);
    }

    /**
     * 检查并解锁成就
     * @param currentStreak 当前连续天数
     * @param totalCompleted 总完成次数
     * @param callback 新解锁成就的回调
     */
    public void checkAndUnlockAchievements(int currentStreak, int totalCompleted, OnAchievementUnlockedCallback callback) {
        AppDatabase.databaseExecutor.execute(() -> {
            List<Achievement> newlyUnlocked = new ArrayList<>();
            long now = System.currentTimeMillis();

            // 检查连续打卡成就
            checkStreakAchievement(Achievement.TYPE_STREAK_7, 7, currentStreak, now, newlyUnlocked);
            checkStreakAchievement(Achievement.TYPE_STREAK_21, 21, currentStreak, now, newlyUnlocked);
            checkStreakAchievement(Achievement.TYPE_STREAK_66, 66, currentStreak, now, newlyUnlocked);

            // 检查累计打卡成就
            checkTotalAchievement(Achievement.TYPE_TOTAL_10, 10, totalCompleted, now, newlyUnlocked);
            checkTotalAchievement(Achievement.TYPE_TOTAL_50, 50, totalCompleted, now, newlyUnlocked);
            checkTotalAchievement(Achievement.TYPE_TOTAL_100, 100, totalCompleted, now, newlyUnlocked);

            // 检查习惯数量成就
            int habitCount = habitDao.getActiveHabitCount(1);
            checkHabitCountAchievement(Achievement.TYPE_FIRST_HABIT, 1, habitCount, now, newlyUnlocked);
            checkHabitCountAchievement(Achievement.TYPE_HABIT_MASTER, 5, habitCount, now, newlyUnlocked);

            if (!newlyUnlocked.isEmpty() && callback != null) {
                callback.onAchievementsUnlocked(newlyUnlocked);
            }
        });
    }

    private void checkStreakAchievement(String type, int required, int current, long timestamp, List<Achievement> newlyUnlocked) {
        if (current >= required) {
            Achievement achievement = achievementDao.getAchievementByType(1, type);
            if (achievement != null && !achievement.isUnlocked()) {
                achievementDao.unlock(achievement.getAchievementId(), timestamp);
                achievement.setUnlockedAt(timestamp);
                newlyUnlocked.add(achievement);
            }
        }
    }

    private void checkTotalAchievement(String type, int required, int current, long timestamp, List<Achievement> newlyUnlocked) {
        if (current >= required) {
            Achievement achievement = achievementDao.getAchievementByType(1, type);
            if (achievement != null && !achievement.isUnlocked()) {
                achievementDao.unlock(achievement.getAchievementId(), timestamp);
                achievement.setUnlockedAt(timestamp);
                newlyUnlocked.add(achievement);
            }
        }
    }

    private void checkHabitCountAchievement(String type, int required, int current, long timestamp, List<Achievement> newlyUnlocked) {
        if (current >= required) {
            Achievement achievement = achievementDao.getAchievementByType(1, type);
            if (achievement != null && !achievement.isUnlocked()) {
                achievementDao.unlock(achievement.getAchievementId(), timestamp);
                achievement.setUnlockedAt(timestamp);
                newlyUnlocked.add(achievement);
            }
        }
    }

    /**
     * 检查完美一周成就
     */
    public void checkPerfectWeekAchievement(boolean isPerfectWeek, OnAchievementUnlockedCallback callback) {
        if (!isPerfectWeek) return;

        AppDatabase.databaseExecutor.execute(() -> {
            Achievement achievement = achievementDao.getAchievementByType(1, Achievement.TYPE_PERFECT_WEEK);
            if (achievement != null && !achievement.isUnlocked()) {
                long now = System.currentTimeMillis();
                achievementDao.unlock(achievement.getAchievementId(), now);
                achievement.setUnlockedAt(now);
                
                List<Achievement> newlyUnlocked = new ArrayList<>();
                newlyUnlocked.add(achievement);
                
                if (callback != null) {
                    callback.onAchievementsUnlocked(newlyUnlocked);
                }
            }
        });
    }

    public interface OnAchievementUnlockedCallback {
        void onAchievementsUnlocked(List<Achievement> achievements);
    }
}
