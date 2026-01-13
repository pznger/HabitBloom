package com.habitbloom.ui.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.habitbloom.data.database.entity.GardenState;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.data.database.entity.Reminder;
import com.habitbloom.data.repository.AchievementRepository;
import com.habitbloom.data.repository.HabitRepository;

import java.util.List;

public class HabitViewModel extends AndroidViewModel {
    private final HabitRepository habitRepository;
    private final AchievementRepository achievementRepository;

    private final LiveData<List<Habit>> allActiveHabits;
    private final MutableLiveData<CheckInResult> checkInResult = new MutableLiveData<>();
    private final MutableLiveData<String> toastMessage = new MutableLiveData<>();

    public HabitViewModel(@NonNull Application application) {
        super(application);
        habitRepository = new HabitRepository(application);
        achievementRepository = new AchievementRepository(application);
        allActiveHabits = habitRepository.getAllActiveHabits();
    }

    // Habit operations
    public LiveData<List<Habit>> getAllActiveHabits() {
        return allActiveHabits;
    }

    public LiveData<Habit> getHabitById(long habitId) {
        return habitRepository.getHabitById(habitId);
    }

    public LiveData<List<Habit>> getHabitsByCategory(String category) {
        return habitRepository.getHabitsByCategory(category);
    }

    public void createHabit(Habit habit) {
        habitRepository.createHabit(habit, habitId -> {
            // 检查首个习惯成就
            achievementRepository.checkAndUnlockAchievements(0, 0, achievements -> {
                if (!achievements.isEmpty()) {
                    toastMessage.postValue("🎉 恭喜获得成就：" + achievements.get(0).getTitle());
                }
            });
        });
    }

    public void updateHabit(Habit habit) {
        habitRepository.updateHabit(habit);
    }

    public void deleteHabit(Habit habit) {
        habitRepository.deleteHabit(habit);
    }

    // Check-in operations
    public void checkIn(long habitId, String notes) {
        habitRepository.checkIn(habitId, notes, new HabitRepository.CheckInCallback() {
            @Override
            public void onSuccess(int newStreak, int growthStage) {
                CheckInResult result = new CheckInResult();
                result.success = true;
                result.newStreak = newStreak;
                result.growthStage = growthStage;
                checkInResult.postValue(result);

                // 获取习惯的总完成次数
                Habit habit = habitRepository.getHabitByIdSync(habitId);
                if (habit != null) {
                    // 检查成就
                    achievementRepository.checkAndUnlockAchievements(
                            newStreak,
                            habit.getTotalCompleted(),
                            achievements -> {
                                if (!achievements.isEmpty()) {
                                    StringBuilder sb = new StringBuilder("🎉 获得新成就：");
                                    for (int i = 0; i < achievements.size(); i++) {
                                        if (i > 0) sb.append("、");
                                        sb.append(achievements.get(i).getTitle());
                                    }
                                    toastMessage.postValue(sb.toString());
                                }
                            }
                    );
                }
            }

            @Override
            public void onAlreadyCheckedIn() {
                CheckInResult result = new CheckInResult();
                result.success = false;
                result.alreadyCheckedIn = true;
                checkInResult.postValue(result);
                toastMessage.postValue("今日已打卡，明天继续加油！");
            }
        });
    }

    public LiveData<CheckInResult> getCheckInResult() {
        return checkInResult;
    }

    public LiveData<String> getToastMessage() {
        return toastMessage;
    }

    // Record operations
    public LiveData<List<HabitRecord>> getRecordsByHabit(long habitId) {
        return habitRepository.getRecordsByHabit(habitId);
    }

    // Garden state operations
    public LiveData<GardenState> getGardenState(long habitId) {
        return habitRepository.getGardenState(habitId);
    }

    public LiveData<List<GardenState>> getAllGardenStates() {
        return habitRepository.getAllGardenStates();
    }

    // Reminder operations
    public LiveData<List<Reminder>> getRemindersByHabit(long habitId) {
        return habitRepository.getRemindersByHabit(habitId);
    }

    public void addReminder(Reminder reminder) {
        habitRepository.addReminder(reminder, null);
    }

    public void updateReminder(Reminder reminder) {
        habitRepository.updateReminder(reminder);
    }

    public void deleteReminder(Reminder reminder) {
        habitRepository.deleteReminder(reminder);
    }

    // Result class
    public static class CheckInResult {
        public boolean success;
        public boolean alreadyCheckedIn;
        public int newStreak;
        public int growthStage;
    }
}
