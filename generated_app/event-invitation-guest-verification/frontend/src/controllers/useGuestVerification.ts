import { useCallback, useState } from 'react';
import type { Guest, VerifyResponse, VerifyStatus } from '../models/types';

const API_BASE_URL = '';

const useGuestVerification = () => {
  const [guest, setGuest] = useState<Guest | null>(null);
  const [status, setStatus] = useState<VerifyStatus>('idle');
  const [message, setMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const verify = useCallback(async (mobileNumber: string): Promise<VerifyResponse> => {
    setIsLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/guests/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobileNumber })
      });

      if (response.status === 200) {
        const data: Guest = await response.json();
        setGuest(data);
        setStatus('authorized');
        setMessage('Verification successful. Welcome!');
        return { status: 'authorized', guest: data };
      }

      if (response.status === 403) {
        setGuest(null);
        setStatus('not_verified');
        const errMsg = 'Your record exists, but it is not yet verified. Please contact the host.';
        setMessage(errMsg);
        return { status: 'not_verified', message: errMsg };
      }

      if (response.status === 404) {
        setGuest(null);
        setStatus('not_authorized');
        const errMsg = 'You are not authorized. Mobile number not found in invited guests list.';
        setMessage(errMsg);
        return { status: 'not_authorized', message: errMsg };
      }

      const errMsg = `Verification failed (${response.status}).`;
      setStatus('error');
      setMessage(errMsg);
      return { status: 'error', message: errMsg };
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Network error';
      setStatus('error');
      setMessage(errMsg);
      return { status: 'error', message: errMsg };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setGuest(null);
    setStatus('idle');
    setMessage('');
  }, []);

  return { guest, status, message, isLoading, verify, reset };
};

export default useGuestVerification;
