package com.habitbloom.ui.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.entity.Achievement;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.repository.AchievementRepository;
import com.habitbloom.data.repository.HabitRepository;
import com.habitbloom.utils.DateUtils;

import java.util.List;

public class StatsViewModel extends AndroidViewModel {
    private final HabitRepository habitRepository;
    private final AchievementRepository achievementRepository;

    private final LiveData<List<Habit>> allHabits;
    private final LiveData<List<Achievement>> unlockedAchievements;
    private final MutableLiveData<StatsData> statsData = new MutableLiveData<>();

    public StatsViewModel(@NonNull Application application) {
        super(application);
        habitRepository = new HabitRepository(application);
        achievementRepository = new AchievementRepository(application);
        allHabits = habitRepository.getAllActiveHabits();
        unlockedAchievements = achievementRepository.getUnlockedAchievements();
    }

    public LiveData<List<Habit>> getAllHabits() {
        return allHabits;
    }

    public LiveData<List<Achievement>> getUnlockedAchievements() {
        return unlockedAchievements;
    }

    public LiveData<StatsData> getStatsData() {
        return statsData;
    }

    public void loadStats() {
        AppDatabase.databaseExecutor.execute(() -> {
            StatsData data = new StatsData();

            // 获取基础统计
            data.totalHabits = habitRepository.getActiveHabitCount();
            data.maxLongestStreak = habitRepository.getMaxLongestStreak();
            data.totalCompletedCount = habitRepository.getTotalCompletedCount();

            // 获取本月完成率
            String monthStart = DateUtils.getMonthStartDate();
            String monthEnd = DateUtils.getMonthEndDate();
            int totalDaysInMonth = DateUtils.getDaysInMonth();
            int currentDay = DateUtils.getDayOfMonth();

            int monthlyCompleted = 0;
            int monthlyTarget = 0;
            
            List<Habit> habits = habitRepository.getAllActiveHabits().getValue();
            if (habits != null) {
                for (Habit habit : habits) {
                    int completed = habitRepository.getCompletedCountInRange(
                            habit.getHabitId(), monthStart, monthEnd);
                    monthlyCompleted += completed;
                    // 目标是每天都完成，到当前日期为止
                    monthlyTarget += currentDay;
                }
            }

            data.monthlyCompletionRate = monthlyTarget > 0 
                    ? (int) ((monthlyCompleted * 100.0) / monthlyTarget) 
                    : 0;

            // 获取成就统计
            data.unlockedAchievements = achievementRepository.getUnlockedCount();
            data.totalAchievements = achievementRepository.getTotalCount();

            statsData.postValue(data);
        });
    }

    public static class StatsData {
        public int totalHabits;
        public int maxLongestStreak;
        public int totalCompletedCount;
        public int monthlyCompletionRate;
        public int unlockedAchievements;
        public int totalAchievements;
    }
}
