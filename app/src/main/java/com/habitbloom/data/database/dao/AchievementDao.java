package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.Achievement;

import java.util.List;

@Dao
public interface AchievementDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Achievement achievement);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Achievement> achievements);

    @Update
    void update(Achievement achievement);

    @Delete
    void delete(Achievement achievement);

    @Query("SELECT * FROM achievements WHERE achievement_id = :achievementId")
    LiveData<Achievement> getAchievementById(long achievementId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId")
    LiveData<List<Achievement>> getAchievementsByUser(long userId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId")
    List<Achievement> getAchievementsByUserSync(long userId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId AND unlocked_at IS NOT NULL ORDER BY unlocked_at DESC")
    LiveData<List<Achievement>> getUnlockedAchievements(long userId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId AND unlocked_at IS NOT NULL ORDER BY unlocked_at DESC")
    List<Achievement> getUnlockedAchievementsSync(long userId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId AND unlocked_at IS NULL")
    List<Achievement> getLockedAchievementsSync(long userId);

    @Query("SELECT * FROM achievements WHERE user_id = :userId AND achievement_type = :type")
    Achievement getAchievementByType(long userId, String type);

    @Query("UPDATE achievements SET unlocked_at = :timestamp WHERE achievement_id = :achievementId")
    void unlock(long achievementId, long timestamp);

    @Query("SELECT COUNT(*) FROM achievements WHERE user_id = :userId AND unlocked_at IS NOT NULL")
    int getUnlockedCount(long userId);

    @Query("SELECT COUNT(*) FROM achievements WHERE user_id = :userId")
    int getTotalCount(long userId);
}
