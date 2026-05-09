import { useCallback, useState } from 'react';
import { Doctor } from '../models/types';

const API_BASE_URL = 'http://localhost:5000';

const useDoctors = () => {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDoctors = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/doctors`);
      if (!response.ok) {
        throw new Error(`Failed to load doctors (${response.status})`);
      }

      const data = await response.json();
      setDoctors(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load doctors');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { doctors, fetchDoctors, isLoading, error };
};

export default useDoctors;