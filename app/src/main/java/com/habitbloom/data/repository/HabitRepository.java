package com.habitbloom.data.repository;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.dao.GardenStateDao;
import com.habitbloom.data.database.dao.HabitDao;
import com.habitbloom.data.database.dao.HabitRecordDao;
import com.habitbloom.data.database.dao.ReminderDao;
import com.habitbloom.data.database.entity.GardenState;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.data.database.entity.Reminder;
import com.habitbloom.utils.DateUtils;

import java.util.List;

public class HabitRepository {
    private final HabitDao habitDao;
    private final HabitRecordDao recordDao;
    private final GardenStateDao gardenStateDao;
    private final ReminderDao reminderDao;

    public HabitRepository(Application application) {
        AppDatabase db = AppDatabase.getDatabase(application);
        habitDao = db.habitDao();
        recordDao = db.habitRecordDao();
        gardenStateDao = db.gardenStateDao();
        reminderDao = db.reminderDao();
    }

    // Habit operations
    public LiveData<List<Habit>> getAllActiveHabits() {
        return habitDao.getActiveHabitsByUser(1);
    }

    public LiveData<List<Habit>> getAllHabits() {
        return habitDao.getAllHabitsByUser(1);
    }

    public LiveData<Habit> getHabitById(long habitId) {
        return habitDao.getHabitById(habitId);
    }

    public Habit getHabitByIdSync(long habitId) {
        return habitDao.getHabitByIdSync(habitId);
    }

    public LiveData<List<Habit>> getHabitsByCategory(String category) {
        return habitDao.getHabitsByCategory(category);
    }

    public void createHabit(Habit habit, Callback<Long> callback) {
        AppDatabase.databaseExecutor.execute(() -> {
            long habitId = habitDao.insert(habit);
            
            // 创建花园状态
            GardenState gardenState = new GardenState();
            gardenState.setHabitId(habitId);
            gardenState.setUserId(1);
            gardenState.setPlantGrowth(0);
            gardenState.setPlantHealth(100);
            gardenState.setStage(1);
            gardenStateDao.insert(gardenState);

            if (callback != null) {
                callback.onComplete(habitId);
            }
        });
    }

    public void updateHabit(Habit habit) {
        AppDatabase.databaseExecutor.execute(() -> habitDao.update(habit));
    }

    public void deleteHabit(Habit habit) {
        AppDatabase.databaseExecutor.execute(() -> {
            habitDao.delete(habit);
            // 级联删除会自动处理相关记录
        });
    }

    public void setHabitActive(long habitId, boolean isActive) {
        AppDatabase.databaseExecutor.execute(() -> habitDao.setActive(habitId, isActive));
    }

    // Record operations
    public LiveData<List<HabitRecord>> getRecordsByHabit(long habitId) {
        return recordDao.getRecordsByHabit(habitId);
    }

    public List<HabitRecord> getRecordsByHabitInRange(long habitId, String startDate, String endDate) {
        return recordDao.getRecordsByHabitInRange(habitId, startDate, endDate);
    }

    public void checkIn(long habitId, String notes, CheckInCallback callback) {
        AppDatabase.databaseExecutor.execute(() -> {
            String today = DateUtils.getTodayString();
            
            // 检查今日是否已打卡
            HabitRecord existingRecord = recordDao.getRecordByHabitAndDate(habitId, today);
            if (existingRecord != null && existingRecord.isCompleted()) {
                if (callback != null) {
                    callback.onAlreadyCheckedIn();
                }
                return;
            }

            // 创建或更新打卡记录
            HabitRecord record = existingRecord != null ? existingRecord : new HabitRecord();
            record.setHabitId(habitId);
            record.setRecordDate(today);
            record.setCompleted(true);
            record.setCompletedTime(DateUtils.getCurrentTimeString());
            record.setNotes(notes);
            recordDao.insert(record);

            // 更新连续天数
            int newStreak = calculateStreak(habitId, today);
            habitDao.updateStreak(habitId, newStreak);
            habitDao.incrementTotalCompleted(habitId);

            // 更新花园状态
            updateGardenState(habitId, newStreak, today);

            Habit habit = habitDao.getHabitByIdSync(habitId);
            if (callback != null) {
                callback.onSuccess(newStreak, habit.getGrowthStage());
            }
        });
    }

    private int calculateStreak(long habitId, String today) {
        // 检查昨天是否打卡
        String yesterday = DateUtils.getYesterdayString();
        HabitRecord yesterdayRecord = recordDao.getRecordByHabitAndDate(habitId, yesterday);
        
        Habit habit = habitDao.getHabitByIdSync(habitId);
        int currentStreak = habit.getCurrentStreak();

        if (yesterdayRecord != null && yesterdayRecord.isCompleted()) {
            // 昨天有打卡，连续天数+1
            return currentStreak + 1;
        } else {
            // 昨天没打卡，重新开始计数
            return 1;
        }
    }

    private void updateGardenState(long habitId, int streak, String date) {
        GardenState state = gardenStateDao.getStateByHabitSync(habitId);
        if (state != null) {
            // 计算生长阶段
            int stage;
            if (streak >= 66) stage = 5;
            else if (streak >= 21) stage = 4;
            else if (streak >= 7) stage = 3;
            else if (streak >= 3) stage = 2;
            else stage = 1;

            // 计算生长进度 (0-100)
            int growth;
            switch (stage) {
                case 1: growth = (int) (streak / 3.0 * 100); break;
                case 2: growth = (int) ((streak - 3) / 4.0 * 100); break;
                case 3: growth = (int) ((streak - 7) / 14.0 * 100); break;
                case 4: growth = (int) ((streak - 21) / 45.0 * 100); break;
                case 5: growth = 100; break;
                default: growth = 0;
            }
            growth = Math.min(100, growth);

            gardenStateDao.updateGrowth(habitId, growth, stage, date);
        }
    }

    public boolean isCompletedToday(long habitId) {
        String today = DateUtils.getTodayString();
        return recordDao.isCompletedToday(habitId, today);
    }

    // Garden state operations
    public LiveData<GardenState> getGardenState(long habitId) {
        return gardenStateDao.getStateByHabit(habitId);
    }

    public LiveData<List<GardenState>> getAllGardenStates() {
        return gardenStateDao.getStatesByUser(1);
    }

    // Reminder operations
    public LiveData<List<Reminder>> getRemindersByHabit(long habitId) {
        return reminderDao.getRemindersByHabit(habitId);
    }

    public void addReminder(Reminder reminder, Callback<Long> callback) {
        AppDatabase.databaseExecutor.execute(() -> {
            long reminderId = reminderDao.insert(reminder);
            if (callback != null) {
                callback.onComplete(reminderId);
            }
        });
    }

    public void updateReminder(Reminder reminder) {
        AppDatabase.databaseExecutor.execute(() -> reminderDao.update(reminder));
    }

    public void deleteReminder(Reminder reminder) {
        AppDatabase.databaseExecutor.execute(() -> reminderDao.delete(reminder));
    }

    // Statistics
    public int getActiveHabitCount() {
        return habitDao.getActiveHabitCount(1);
    }

    public int getMaxLongestStreak() {
        return habitDao.getMaxLongestStreak(1);
    }

    public int getTotalCompletedCount() {
        return habitDao.getTotalCompletedCount(1);
    }

    public int getCompletedCountInRange(long habitId, String startDate, String endDate) {
        return recordDao.getCompletedCountInRange(habitId, startDate, endDate);
    }

    // Callbacks
    public interface Callback<T> {
        void onComplete(T result);
    }

    public interface CheckInCallback {
        void onSuccess(int newStreak, int growthStage);
        void onAlreadyCheckedIn();
    }
}
