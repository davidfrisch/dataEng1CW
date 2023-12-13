export interface run_summary {
  run_id: string;
  status: string;
  score_std: number;
  score_gmean: number;
  duration: number;
  date_started: string;
  date_finished: string;
  author: string;
}