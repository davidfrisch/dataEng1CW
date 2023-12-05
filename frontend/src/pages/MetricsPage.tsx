
type Props = {};

export default function MetricsPage({}: Props) {

  return (
    <div style={{ width: "100%" }}>
      <iframe src="http://localhost:8080" width="100%" height="600"></iframe>
    </div>
  );
}
