import { useCallback, useState } from 'react';
import { Booking } from '../models/types';

const API_BASE_URL = 'http://localhost:5000';

export const useAdmin = () => {
  const [appointments, setAppointments] = useState<Booking[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAppointments = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/appointments`);
      if (!response.ok) {
        throw new Error(`Failed to load appointments (${response.status})`);
      }

      const data = await response.json();
      setAppointments(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load appointments');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateAppointmentStatus = useCallback(
    async (bookingRef: string, action: 'approve' | 'cancel') => {
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/api/admin/appointments/${bookingRef}/${action}`, {
          method: 'POST',
        });

        if (!response.ok) {
          throw new Error(`Failed to ${action} appointment (${response.status})`);
        }

        await fetchAppointments();
      } catch (err) {
        setError(err instanceof Error ? err.message : `Failed to ${action} appointment`);
      }
    },
    [fetchAppointments]
  );

  return { appointments, fetchAppointments, updateAppointmentStatus, isLoading, error };
};