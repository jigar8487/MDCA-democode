import React from 'react';
import type { VerifyStatus } from '../../models/types';

interface StatusMessageProps {
  status: VerifyStatus;
  message: string;
}

const StatusMessage: React.FC<StatusMessageProps> = ({ status, message }) => {
  if (status === 'idle' || !message) return null;

  const className =
    status === 'authorized'
      ? 'state-card success'
      : status === 'not_verified' || status === 'not_authorized' || status === 'error'
      ? 'state-card error'
      : 'state-card';

  return <p className={className}>{message}</p>;
};

export default StatusMessage;
