import React, { useEffect, useRef } from "react";

type Props = {};

export default function MetricsPage({}: Props) {

  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    // replace host with localhost
    const iframe = iframeRef.current;
    // take the current url
    if (!iframe) return;
    const url = new URL(iframe.src);
    // if host hast port 8080
    if (url.host.includes(":4040")) {
      // replace host with localhost
      console.log(url.host);
      url.host = "localhost:4040";
      // set the new url
      iframe.src = url.toString();
    }
    

  }, []);
  

  return (
    <div style={{ width: "100%" }}>
      <iframe ref={iframeRef} src="http://localhost:8080" width="100%" height="600"></iframe>
    </div>
  );
}
