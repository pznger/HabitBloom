package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.GardenState;

import java.util.List;

@Dao
public interface GardenStateDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(GardenState state);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<GardenState> states);

    @Update
    void update(GardenState state);

    @Delete
    void delete(GardenState state);

    @Query("SELECT * FROM garden_states WHERE state_id = :stateId")
    LiveData<GardenState> getStateById(long stateId);

    @Query("SELECT * FROM garden_states WHERE habit_id = :habitId")
    LiveData<GardenState> getStateByHabit(long habitId);

    @Query("SELECT * FROM garden_states WHERE habit_id = :habitId")
    GardenState getStateByHabitSync(long habitId);

    @Query("SELECT * FROM garden_states WHERE user_id = :userId")
    LiveData<List<GardenState>> getStatesByUser(long userId);

    @Query("SELECT * FROM garden_states WHERE user_id = :userId")
    List<GardenState> getStatesByUserSync(long userId);

    @Query("UPDATE garden_states SET plant_growth = :growth, stage = :stage, last_watered = :date WHERE habit_id = :habitId")
    void updateGrowth(long habitId, int growth, int stage, String date);

    @Query("UPDATE garden_states SET plant_health = :health WHERE habit_id = :habitId")
    void updateHealth(long habitId, int health);

    @Query("UPDATE garden_states SET last_watered = :date WHERE habit_id = :habitId")
    void updateLastWatered(long habitId, String date);

    @Query("DELETE FROM garden_states WHERE habit_id = :habitId")
    void deleteByHabitId(long habitId);
}
