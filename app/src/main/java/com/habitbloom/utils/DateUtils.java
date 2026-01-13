package com.habitbloom.utils;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class DateUtils {
    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
    private static final SimpleDateFormat TIME_FORMAT = new SimpleDateFormat("HH:mm", Locale.getDefault());
    private static final SimpleDateFormat DATE_TIME_FORMAT = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault());
    private static final SimpleDateFormat DISPLAY_DATE_FORMAT = new SimpleDateFormat("MM月dd日", Locale.getDefault());
    private static final SimpleDateFormat DISPLAY_DATE_FULL_FORMAT = new SimpleDateFormat("yyyy年MM月dd日", Locale.getDefault());

    public static String getTodayString() {
        return DATE_FORMAT.format(new Date());
    }

    public static String getYesterdayString() {
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DAY_OF_MONTH, -1);
        return DATE_FORMAT.format(cal.getTime());
    }

    public static String getCurrentTimeString() {
        return TIME_FORMAT.format(new Date());
    }

    public static String formatDate(Date date) {
        return DATE_FORMAT.format(date);
    }

    public static String formatTime(Date date) {
        return TIME_FORMAT.format(date);
    }

    public static String formatDateTime(Date date) {
        return DATE_TIME_FORMAT.format(date);
    }

    public static String formatDisplayDate(Date date) {
        return DISPLAY_DATE_FORMAT.format(date);
    }

    public static String formatDisplayDateFull(Date date) {
        return DISPLAY_DATE_FULL_FORMAT.format(date);
    }

    public static String formatTimestamp(long timestamp) {
        return DATE_TIME_FORMAT.format(new Date(timestamp));
    }

    public static Date parseDate(String dateStr) {
        try {
            return DATE_FORMAT.parse(dateStr);
        } catch (Exception e) {
            return null;
        }
    }

    public static String getWeekStartDate() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.DAY_OF_WEEK, Calendar.SUNDAY);
        return DATE_FORMAT.format(cal.getTime());
    }

    public static String getWeekEndDate() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.DAY_OF_WEEK, Calendar.SATURDAY);
        return DATE_FORMAT.format(cal.getTime());
    }

    public static String getMonthStartDate() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.DAY_OF_MONTH, 1);
        return DATE_FORMAT.format(cal.getTime());
    }

    public static String getMonthEndDate() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.DAY_OF_MONTH, cal.getActualMaximum(Calendar.DAY_OF_MONTH));
        return DATE_FORMAT.format(cal.getTime());
    }

    public static String getDateOffset(int days) {
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DAY_OF_MONTH, days);
        return DATE_FORMAT.format(cal.getTime());
    }

    public static int getDayOfWeek() {
        return Calendar.getInstance().get(Calendar.DAY_OF_WEEK);
    }

    public static int getDayOfMonth() {
        return Calendar.getInstance().get(Calendar.DAY_OF_MONTH);
    }

    public static int getDaysInMonth() {
        return Calendar.getInstance().getActualMaximum(Calendar.DAY_OF_MONTH);
    }

    public static String getGreeting() {
        int hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY);
        if (hour < 6) return "凌晨好";
        if (hour < 9) return "早上好";
        if (hour < 12) return "上午好";
        if (hour < 14) return "中午好";
        if (hour < 18) return "下午好";
        if (hour < 22) return "晚上好";
        return "夜深了";
    }

    public static String getDateString(int year, int month, int day) {
        return String.format(Locale.getDefault(), "%04d-%02d-%02d", year, month + 1, day);
    }

    public static long daysBetween(String date1, String date2) {
        try {
            Date d1 = DATE_FORMAT.parse(date1);
            Date d2 = DATE_FORMAT.parse(date2);
            if (d1 != null && d2 != null) {
                long diff = Math.abs(d2.getTime() - d1.getTime());
                return diff / (24 * 60 * 60 * 1000);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 0;
    }

    public static boolean isToday(String dateStr) {
        return getTodayString().equals(dateStr);
    }

    public static boolean isYesterday(String dateStr) {
        return getYesterdayString().equals(dateStr);
    }
}
