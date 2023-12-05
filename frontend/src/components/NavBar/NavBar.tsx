import './styles.css'
type Props = {};

export default function NavBar({}: Props) {

  function goToRuns() {
    window.location.href = "/";
  }

  function goToUpload() {
    window.location.href = "/upload";
  }

  function goToMetrics() {
    window.location.href = "/metrics";
  }


  return (
    <div className="navbar">
      <button className="nav-button" onClick={goToUpload}>Upload</button>
      <button className="nav-button" onClick={goToRuns}>Runs</button>
      <button className="nav-button" onClick={goToMetrics}>Metrics</button>
    </div>
  );
}
