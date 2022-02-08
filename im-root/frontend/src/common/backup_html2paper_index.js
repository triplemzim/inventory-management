/*eslint-disable*/

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });

function addStyles(win, styles) {
  styles.forEach((style) => {
    let link = win.document.createElement("link");
    link.setAttribute("rel", "stylesheet");
    link.setAttribute("type", "text/css");
    link.setAttribute("href", style);
    win.document.getElementsByTagName("head")[0].appendChild(link);
  });
}

function openWindow(url, name, props) {
  let windowRef = null;
  windowRef = window.open(url, name, props);
  if (!windowRef.opener) {
    windowRef.opener = self;
  }
  windowRef.focus();
  return windowRef;
}

const VueHtmlToPaper = {
  install(_i, options = {}) {
    let globals = _i.prototype || _i.config.globalProperties;
    globals.$htmlToPaper = (el, localOptions, cb = () => true) => {
      let defaultName = "_blank",
        defaultSpecs = ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
        defaultReplace = true,
        defaultStyles = [];
      let {
        name = defaultName,
        specs = defaultSpecs,
        replace = defaultReplace,
        styles = defaultStyles,
      } = options;

      // If has localOptions
      if (localOptions) {
        if (localOptions.name) name = localOptions.name;
        if (localOptions.specs) specs = localOptions.specs;
        if (localOptions.replace) replace = localOptions.replace;
        if (localOptions.styles) styles = localOptions.styles;
      }

      specs = specs.length ? specs.join(",") : "";

      const element = window.document.getElementById(el);

      if (!element) {
        alert(`Element to print #${el} not found!`);
        return;
      }

      const url = "";
      const win = openWindow(url, name, specs);

      win.document.write(`
        <html>
          <head>
            <title></title>
          </head>
          <body>
            ${element.innerHTML}
          </body>
        </html>
      `);

      addStyles(win, styles);

      setTimeout(() => {
        win.document.close();
        win.focus();
        win.print();
        setTimeout(function () {
          window.close();
        }, 1);
        cb();
      }, 1000);

      return true;
    };
  },
};

exports.default = VueHtmlToPaper;