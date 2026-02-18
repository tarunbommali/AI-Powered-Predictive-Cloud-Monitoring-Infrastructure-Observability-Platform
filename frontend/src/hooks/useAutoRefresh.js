import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for debounced API calls with configurable auto-refresh interval
 * @param {Function} fetchFn - The async function to call
 * @param {number} refreshInterval - Interval in seconds (0 = disabled)
 * @param {number} debounceMs - Debounce delay in milliseconds
 * @param {Array} deps - Dependencies that trigger a re-fetch
 */
export const useAutoRefresh = (fetchFn, refreshInterval = 15, debounceMs = 300, deps = []) => {
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [interval, setInterval_] = useState(refreshInterval);
    const timeoutRef = useRef(null);
    const intervalRef = useRef(null);
    const lastCallRef = useRef(0);

    const debouncedFetch = useCallback(async (isManual = false) => {
        const now = Date.now();
        const timeSinceLastCall = now - lastCallRef.current;

        // Debounce: skip if called too recently (unless it's first load)
        if (timeSinceLastCall < debounceMs && lastCallRef.current !== 0 && !isManual) {
            return;
        }

        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        const delay = isManual ? 0 : Math.max(0, debounceMs - timeSinceLastCall);

        return new Promise((resolve) => {
            timeoutRef.current = setTimeout(async () => {
                if (isManual) setRefreshing(true);
                lastCallRef.current = Date.now();

                try {
                    await fetchFn();
                } catch (err) {
                    console.error('Auto-refresh fetch error:', err);
                } finally {
                    setLoading(false);
                    setRefreshing(false);
                    resolve();
                }
            }, delay);
        });
    }, [fetchFn, debounceMs]);

    // Initial fetch + re-fetch on deps change
    useEffect(() => {
        debouncedFetch();
    }, [...deps, debouncedFetch]);

    // Auto-refresh interval
    useEffect(() => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }

        if (interval > 0) {
            intervalRef.current = setInterval(() => {
                debouncedFetch();
            }, interval * 1000);
        }

        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, [interval, debouncedFetch]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (timeoutRef.current) clearTimeout(timeoutRef.current);
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, []);

    const manualRefresh = useCallback(() => {
        debouncedFetch(true);
    }, [debouncedFetch]);

    return {
        loading,
        refreshing,
        refreshInterval: interval,
        setRefreshInterval: setInterval_,
        manualRefresh,
    };
};

/**
 * Refresh interval options for the selector
 */
export const REFRESH_OPTIONS = [
    { label: 'Off', value: 0 },
    { label: '5s', value: 5 },
    { label: '10s', value: 10 },
    { label: '15s', value: 15 },
    { label: '30s', value: 30 },
    { label: '60s', value: 60 },
];
