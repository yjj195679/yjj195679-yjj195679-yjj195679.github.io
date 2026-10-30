// Build-time only: HTML + MathML remain readable without browser JavaScript.
const katex = require('../js/vendor/katex/katex.min.js');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  const expressions = JSON.parse(input);
  process.stdout.write(JSON.stringify(Object.fromEntries(expressions.map(tex => [tex,
    katex.renderToString(tex, {throwOnError:true, strict:'error', trust:false, output:'htmlAndMathml'})
  ]))));
});
