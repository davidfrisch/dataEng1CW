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
    window.open("http://ec2-18-130-66-138.eu-west-2.compute.amazonaws.com/spark-master", "_blank");
  }

  function goToSearch() {
    window.location.href = "/search";
  }


  return (
    <div className="navbar">
      <button className="nav-button" onClick={goToUpload}>Upload</button>
      <button className="nav-button" onClick={goToSearch}>Search</button>
      <button className="nav-button" onClick={goToRuns}>Runs</button>
      <button className="nav-button" onClick={goToMetrics}>Metrics</button>
    </div>
  );
}
