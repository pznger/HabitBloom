package com.habitbloom.ui.stats;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;
import com.habitbloom.data.database.entity.Achievement;
import com.habitbloom.utils.DateUtils;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class AchievementAdapter extends RecyclerView.Adapter<AchievementAdapter.AchievementViewHolder> {

    private List<Achievement> achievements = new ArrayList<>();

    public void setAchievements(List<Achievement> achievements) {
        this.achievements = achievements;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public AchievementViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_achievement, parent, false);
        return new AchievementViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull AchievementViewHolder holder, int position) {
        Achievement achievement = achievements.get(position);
        holder.bind(achievement);
    }

    @Override
    public int getItemCount() {
        return achievements.size();
    }

    static class AchievementViewHolder extends RecyclerView.ViewHolder {
        private final TextView tvBadge;
        private final TextView tvTitle;
        private final TextView tvDescription;
        private final TextView tvUnlockDate;

        AchievementViewHolder(@NonNull View itemView) {
            super(itemView);
            tvBadge = itemView.findViewById(R.id.tv_badge);
            tvTitle = itemView.findViewById(R.id.tv_title);
            tvDescription = itemView.findViewById(R.id.tv_description);
            tvUnlockDate = itemView.findViewById(R.id.tv_unlock_date);
        }

        void bind(Achievement achievement) {
            tvBadge.setText(achievement.getBadgeIcon());
            tvTitle.setText(achievement.getTitle());
            tvDescription.setText(achievement.getDescription());

            if (achievement.getUnlockedAt() != null) {
                Date date = new Date(achievement.getUnlockedAt());
                tvUnlockDate.setText(DateUtils.formatDisplayDate(date));
                tvUnlockDate.setVisibility(View.VISIBLE);
            } else {
                tvUnlockDate.setVisibility(View.GONE);
            }
        }
    }
}
