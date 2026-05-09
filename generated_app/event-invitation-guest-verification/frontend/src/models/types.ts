export interface Event {
  id: number;
  title: string;
  dateTimeUtc: string;
  venue: string;
  description: string;
  host: string;
}

export interface Guest {
  id: number;
  name: string;
  mobileNumber: string;
  isVerified: boolean;
  eventId: number;
  event?: Event | null;
}

export type VerifyStatus = 'idle' | 'authorized' | 'not_verified' | 'not_authorized' | 'error';

export interface VerifyResponse {
  status: VerifyStatus;
  guest?: Guest;
  message?: string;
}
