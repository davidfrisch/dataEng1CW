import { useState, useEffect } from "react";
import "./styles.css";
type TimerProps = {
  startDateTime: string;
};

const Timer = ({ startDateTime }: TimerProps) => {
  const [elapsedTime, setElapsedTime] = useState(calculateElapsedTime());

  useEffect(() => {
    const timerInterval = setInterval(() => {
      setElapsedTime(calculateElapsedTime());
    }, 1000);

    return () => {
      clearInterval(timerInterval);
    };
  }, [startDateTime]);

  function calculateElapsedTime() {
    // Sun Dec 17 2023 16:32:39 GMT+0100 (Central European Standard Time)

    const startDate = new Date(startDateTime) as any;
    const now = new Date();

    const timeZoneOffset = startDate.getTimezoneOffset() as number;
    const startDateAdjusted = new Date(startDate.getTime() - timeZoneOffset * 60 * 1000);

    const elapsedTime = now.getTime() - startDateAdjusted.getTime();

    const seconds = Math.floor(elapsedTime / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    return {
      days,
      hours: hours % 24,
      minutes: minutes % 60,
      seconds: seconds % 60,
    };
  }

  return (
    <div className="timer">
      {elapsedTime.days > 0 && <p className="timer-item">{elapsedTime.days} days</p>}
      {elapsedTime.hours > 0 && <p className="timer-item">{elapsedTime.hours} hours</p>}
      <p className="timer-item">{elapsedTime.minutes} minutes</p>
      <p className="timer-item">{elapsedTime.seconds} seconds</p>
    </div>
  );
};

export default Timer;
