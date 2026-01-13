package com.habitbloom.ui.habit;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;
import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.utils.DateUtils;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CalendarAdapter extends RecyclerView.Adapter<CalendarAdapter.DayViewHolder> {

    private final long habitId;
    private final List<DayItem> days = new ArrayList<>();
    private final Set<String> completedDates = new HashSet<>();
    private final String today;

    public CalendarAdapter(long habitId) {
        this.habitId = habitId;
        this.today = DateUtils.getTodayString();
        generateDays();
        loadCompletedDates();
    }

    private void generateDays() {
        Calendar calendar = Calendar.getInstance();
        int currentDay = calendar.get(Calendar.DAY_OF_MONTH);
        int daysInMonth = calendar.getActualMaximum(Calendar.DAY_OF_MONTH);

        // Add day names header
        String[] dayNames = {"日", "一", "二", "三", "四", "五", "六"};
        for (String name : dayNames) {
            days.add(new DayItem(name, true, false));
        }

        // Get first day of month
        calendar.set(Calendar.DAY_OF_MONTH, 1);
        int firstDayOfWeek = calendar.get(Calendar.DAY_OF_WEEK) - 1; // 0 = Sunday

        // Add empty cells for alignment
        for (int i = 0; i < firstDayOfWeek; i++) {
            days.add(new DayItem("", false, false));
        }

        // Add days of month
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        for (int day = 1; day <= daysInMonth; day++) {
            String dateStr = DateUtils.getDateString(year, month, day);
            boolean isToday = dateStr.equals(today);
            days.add(new DayItem(String.valueOf(day), false, isToday, dateStr));
        }
    }

    private void loadCompletedDates() {
        AppDatabase.databaseExecutor.execute(() -> {
            String monthStart = DateUtils.getMonthStartDate();
            String monthEnd = DateUtils.getMonthEndDate();
            
            List<HabitRecord> records = AppDatabase.getDatabase(null)
                    .habitRecordDao()
                    .getRecordsByHabitInRange(habitId, monthStart, monthEnd);
            
            for (HabitRecord record : records) {
                if (record.isCompleted()) {
                    completedDates.add(record.getRecordDate());
                }
            }
        });
    }

    @NonNull
    @Override
    public DayViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_calendar_day, parent, false);
        return new DayViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DayViewHolder holder, int position) {
        DayItem item = days.get(position);
        holder.bind(item, completedDates.contains(item.dateStr));
    }

    @Override
    public int getItemCount() {
        return days.size();
    }

    static class DayViewHolder extends RecyclerView.ViewHolder {
        private final TextView tvDay;

        DayViewHolder(@NonNull View itemView) {
            super(itemView);
            tvDay = itemView.findViewById(R.id.tv_day);
        }

        void bind(DayItem item, boolean isCompleted) {
            tvDay.setText(item.text);

            if (item.isHeader) {
                tvDay.setTextColor(Color.parseColor("#757575"));
                tvDay.setBackgroundColor(Color.TRANSPARENT);
            } else if (item.text.isEmpty()) {
                tvDay.setBackgroundColor(Color.TRANSPARENT);
            } else if (isCompleted) {
                tvDay.setBackgroundResource(R.drawable.day_completed_background);
                tvDay.setTextColor(Color.WHITE);
            } else if (item.isToday) {
                tvDay.setBackgroundResource(R.drawable.day_today_background);
                tvDay.setTextColor(Color.parseColor("#4CAF50"));
            } else {
                tvDay.setBackgroundColor(Color.TRANSPARENT);
                tvDay.setTextColor(Color.parseColor("#212121"));
            }
        }
    }

    static class DayItem {
        String text;
        boolean isHeader;
        boolean isToday;
        String dateStr;

        DayItem(String text, boolean isHeader, boolean isToday) {
            this.text = text;
            this.isHeader = isHeader;
            this.isToday = isToday;
            this.dateStr = "";
        }

        DayItem(String text, boolean isHeader, boolean isToday, String dateStr) {
            this.text = text;
            this.isHeader = isHeader;
            this.isToday = isToday;
            this.dateStr = dateStr;
        }
    }
}
