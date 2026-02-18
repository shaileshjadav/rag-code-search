import { useState } from "react";
import { GlobalStyle } from "./App.style";
import { useEffect } from "react";
import { getSelector } from "./utils/helper";
import Hover from "./components/Hover/Hover";
import Button from "./components/Button/Button";
import Message from "./components/MessageBox/Message";

function App() {
  const [hoverSelector, setHoverSelector] = useState(false);
  const [height, setHeight] = useState("");
  const [width, setWidth] = useState("");
  const [top, setTop] = useState("");
  const [left, setLeft] = useState(false);
  const [isoutOfBody, setIsoutOfBody] = useState(false);
  const [isStart, setIsStart] = useState(true);
  const [infoMessage, setInfoMessage] = useState('');
  const [selectors, setSelectors] = useState([]);

  useEffect(() => {
    const handleHover = (e) => {
      const selector = getSelector(e.target);

      if (selector) {
        const currEle = document.querySelector(selector);
        const width = currEle.offsetWidth;
        const height = currEle.offsetHeight;
        const viewportOffset = e.target.getBoundingClientRect();
        setHoverSelector(selector);
        setWidth(width);
        setHeight(height);
        setTop(viewportOffset.top);
        setLeft(viewportOffset.left);
        setIsoutOfBody(viewportOffset.top <= 20 ? true : false);
      }
    };

    const handleClick = (e) => {
      const rootContainer = document.querySelector("#react-app")
      const outSideOfRoot = !rootContainer.contains(e.target);
      if (outSideOfRoot) {
        // stop to navigate
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        
        // copy to clipboard
        setIsStart(false);
        const newSelectors = [...selectors, hoverSelector];
        setSelectors(newSelectors);
        const allSelectors = newSelectors.join('> ');

        navigator.clipboard.writeText(allSelectors)
        .then(() => {
            setInfoMessage(`Copied Selector: ${allSelectors}`)
        })
        .catch(err => {
          console.error("Failed to copy text: ", err);
        });
      }
    };
    if (isStart) {
      // register dom events
      document.addEventListener("mouseover", handleHover, false);
      document.addEventListener("click", handleClick, true);
    } else {
      document.removeEventListener("mouseover", handleHover, false);
      document.removeEventListener("click", handleClick, true);
    }

    return () => {
      document.removeEventListener("mouseover", handleHover, false);
      document.removeEventListener("click", handleClick, true);
    };
  }, [isStart, hoverSelector, selectors]);

  return (
    <div>
      <GlobalStyle />
      {!isStart && <Button text="Continue" onClick={() => setIsStart(true)}/>}
      {isStart && (
        <Hover
        width={width}
        height={height}
        top={top}
        left={left}
        hoverSelector={hoverSelector}
        isoutOfBody={isoutOfBody}
      />
      )}

    {infoMessage && <Message message={infoMessage} onClose={()=>setInfoMessage('')}/>}
      
    </div>
  );
}

export default App;

