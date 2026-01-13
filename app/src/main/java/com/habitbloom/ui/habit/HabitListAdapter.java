package com.habitbloom.ui.habit;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.card.MaterialCardView;
import com.habitbloom.R;
import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.utils.Constants;
import com.habitbloom.utils.DateUtils;

import java.util.ArrayList;
import java.util.List;

public class HabitListAdapter extends RecyclerView.Adapter<HabitListAdapter.HabitViewHolder> {

    private List<Habit> habits = new ArrayList<>();
    private final OnHabitClickListener listener;

    public interface OnHabitClickListener {
        void onHabitClick(Habit habit);
    }

    public HabitListAdapter(OnHabitClickListener listener) {
        this.listener = listener;
    }

    public void setHabits(List<Habit> habits) {
        this.habits = habits;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public HabitViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_habit_list, parent, false);
        return new HabitViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull HabitViewHolder holder, int position) {
        Habit habit = habits.get(position);
        holder.bind(habit);
    }

    @Override
    public int getItemCount() {
        return habits.size();
    }

    class HabitViewHolder extends RecyclerView.ViewHolder {
        private final MaterialCardView cardHabit;
        private final TextView tvIcon;
        private final TextView tvName;
        private final TextView tvCategory;
        private final ProgressBar progressBar;
        private final TextView tvStreak;
        private final ImageView ivCheck;

        HabitViewHolder(@NonNull View itemView) {
            super(itemView);
            cardHabit = itemView.findViewById(R.id.card_habit);
            tvIcon = itemView.findViewById(R.id.tv_icon);
            tvName = itemView.findViewById(R.id.tv_name);
            tvCategory = itemView.findViewById(R.id.tv_category);
            progressBar = itemView.findViewById(R.id.progress_bar);
            tvStreak = itemView.findViewById(R.id.tv_streak);
            ivCheck = itemView.findViewById(R.id.iv_check);
        }

        void bind(Habit habit) {
            String plantIcon = Constants.getPlantIcon(habit.getPlantType(), habit.getGrowthStage());
            tvIcon.setText(plantIcon);
            tvName.setText(habit.getName());
            tvCategory.setText(Constants.getCategoryIcon(habit.getCategory()) + " " + 
                    Constants.getCategoryName(habit.getCategory()));

            if (habit.getCurrentStreak() > 0) {
                tvStreak.setText("连续" + habit.getCurrentStreak() + "天");
            } else {
                tvStreak.setText(habit.getGrowthStageName());
            }

            int progress = calculateProgress(habit.getCurrentStreak());
            progressBar.setProgress(progress);

            // Check if completed today
            AppDatabase.databaseExecutor.execute(() -> {
                String today = DateUtils.getTodayString();
                HabitRecord record = AppDatabase.getDatabase(itemView.getContext())
                        .habitRecordDao()
                        .getRecordByHabitAndDate(habit.getHabitId(), today);
                
                boolean isCompletedToday = record != null && record.isCompleted();
                itemView.post(() -> {
                    ivCheck.setVisibility(isCompletedToday ? View.VISIBLE : View.GONE);
                });
            });

            cardHabit.setOnClickListener(v -> {
                if (listener != null) {
                    listener.onHabitClick(habit);
                }
            });
        }

        private int calculateProgress(int streak) {
            if (streak >= 66) return 100;
            if (streak >= 21) return (int) ((streak - 21) / 45.0 * 100);
            if (streak >= 7) return (int) ((streak - 7) / 14.0 * 100);
            if (streak >= 3) return (int) ((streak - 3) / 4.0 * 100);
            return (int) (streak / 3.0 * 100);
        }
    }
}
