import { useCallback, useState } from 'react';
import type { Event } from '../models/types';

const API_BASE_URL = '';

const useEvent = () => {
  const [event, setEvent] = useState<Event | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEvent = useCallback(async (id: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/events/${id}`);
      if (!response.ok) {
        throw new Error(`Failed to load event (${response.status})`);
      }
      const data: Event = await response.json();
      setEvent(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load event');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { event, fetchEvent, isLoading, error };
};

export default useEvent;
