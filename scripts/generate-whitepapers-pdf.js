#!/usr/bin/env node

/**
 * Whitepaper PDF Generator
 * Generates executive-grade PDFs from markdown whitepapers
 *
 * Requirements:
 * - npm install puppeteer marked
 *
 * Usage:
 * - node scripts/generate-whitepapers-pdf.js
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const { marked } = require('marked');

// Configuration
const WHITEPAPERS = [
  {
    name: 'omega-governed-execution',
    input: path.join(__dirname, '../whitepapers/omega-governed-execution.md'),
    output: path.join(__dirname, '../assets/whitepapers/omega-governed-execution-v1.0.0.pdf'),
    title: 'OMEGA Governed Execution',
    subtitle: 'Artifact-Registered & Cryptographically Resumed Workflows',
    coverLine: 'Implements: Cryptographically Governed AI Execution (CGAE)',
    footerText: 'Governed by Keon (CGAE v1.0.0)',
    footerLogo: path.join(__dirname, '../../keon-systems-web/public/images/keon-cube-cyan.png'),
    watermark: null // No full-page watermark for OMEGA
  },
  {
    name: 'cgae',
    input: path.join(__dirname, '../../keon-docs/docs/whitepapers/cgae/v1.0.0.md'),
    output: path.join(__dirname, '../assets/whitepapers/cgae-v1.0.0.pdf'),
    title: 'Cryptographically Governed AI Execution',
    subtitle: 'A New Category for Enterprise-Grade Autonomous Systems',
    coverLine: null,
    footerText: 'Keon Systems',
    footerLogo: path.join(__dirname, '../../keon-systems-web/public/images/keon-cube-cyan.png'),
    watermark: path.join(__dirname, '../../keon-systems-web/public/images/keon-cube-cyan.png')
  }
];

// CSS Styles for executive-grade formatting
const getStyles = (hasWatermark) => `
<style>
  @page {
    size: Letter;
    margin: 1in 0.75in;
  }

  body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
    ${hasWatermark ? `
      background-image: url('file://${hasWatermark}');
      background-repeat: no-repeat;
      background-position: center center;
      background-size: 60%;
      background-attachment: fixed;
      background-opacity: 0.04;
    ` : ''}
  }

  h1 {
    font-size: 24pt;
    font-weight: 700;
    margin-top: 24pt;
    margin-bottom: 12pt;
    color: #0a0a0a;
    page-break-after: avoid;
  }

  h2 {
    font-size: 18pt;
    font-weight: 600;
    margin-top: 20pt;
    margin-bottom: 10pt;
    color: #1a1a1a;
    page-break-after: avoid;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 6pt;
  }

  h3 {
    font-size: 14pt;
    font-weight: 600;
    margin-top: 16pt;
    margin-bottom: 8pt;
    color: #2a2a2a;
    page-break-after: avoid;
  }

  p {
    margin-bottom: 10pt;
    text-align: justify;
  }

  ul, ol {
    margin-bottom: 10pt;
    padding-left: 24pt;
  }

  li {
    margin-bottom: 6pt;
  }

  blockquote {
    margin: 16pt 0;
    padding: 12pt 20pt;
    background: #f8f8f8;
    border-left: 4pt solid #16c79a;
    font-style: italic;
    page-break-inside: avoid;
  }

  code {
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 9pt;
    background: #f5f5f5;
    padding: 2pt 4pt;
    border-radius: 2pt;
  }

  pre {
    background: #f8f8f8;
    padding: 12pt;
    border-radius: 4pt;
    overflow-x: auto;
    page-break-inside: avoid;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0;
    page-break-inside: avoid;
  }

  th, td {
    border: 1pt solid #d0d0d0;
    padding: 8pt;
    text-align: left;
  }

  th {
    background: #f0f0f0;
    font-weight: 600;
  }

  hr {
    border: none;
    border-top: 1pt solid #d0d0d0;
    margin: 20pt 0;
  }

  .cover-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    text-align: center;
    page-break-after: always;
  }

  .cover-title {
    font-size: 36pt;
    font-weight: 700;
    margin-bottom: 16pt;
    color: #0a0a0a;
  }

  .cover-subtitle {
    font-size: 18pt;
    font-weight: 400;
    margin-bottom: 32pt;
    color: #4a4a4a;
  }

  .cover-line {
    font-size: 14pt;
    font-weight: 600;
    margin-top: 48pt;
    color: #16c79a;
    padding: 12pt 24pt;
    border: 2pt solid #16c79a;
    border-radius: 4pt;
  }

  .cover-meta {
    font-size: 11pt;
    color: #6a6a6a;
    margin-top: 64pt;
  }

  @media print {
    .page-footer {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 40pt;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 0.75in;
      border-top: 1pt solid #e0e0e0;
      font-size: 9pt;
      color: #6a6a6a;
    }

    .footer-logo {
      height: 20pt;
      opacity: 0.7;
    }

    .footer-text {
      flex: 1;
      text-align: center;
    }

    .footer-page {
      text-align: right;
    }
  }
</style>
`;

// Generate cover page HTML
function generateCoverPage(config) {
  const today = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return `
    <div class="cover-page">
      <div class="cover-title">${config.title}</div>
      <div class="cover-subtitle">${config.subtitle}</div>
      ${config.coverLine ? `<div class="cover-line">${config.coverLine}</div>` : ''}
      <div class="cover-meta">
        Version 1.0.0<br/>
        Published: ${today}<br/>
        Status: Canonical
      </div>
    </div>
  `;
}

// Generate footer HTML
function generateFooter(config) {
  if (!config.footerLogo || !fs.existsSync(config.footerLogo)) {
    return `
      <div class="page-footer">
        <div class="footer-text">${config.footerText}</div>
        <div class="footer-page"><span class="pageNumber"></span></div>
      </div>
    `;
  }

  const logoBase64 = fs.readFileSync(config.footerLogo).toString('base64');
  const logoExt = path.extname(config.footerLogo).slice(1);

  return `
    <div class="page-footer">
      <img src="data:image/${logoExt};base64,${logoBase64}" class="footer-logo" />
      <div class="footer-text">${config.footerText}</div>
      <div class="footer-page"><span class="pageNumber"></span></div>
    </div>
  `;
}

// Main PDF generation function
async function generatePDF(config) {
  console.log(`\n📄 Generating PDF: ${config.name}`);
  console.log(`   Input:  ${config.input}`);
  console.log(`   Output: ${config.output}`);

  // Read markdown content
  if (!fs.existsSync(config.input)) {
    console.error(`   ❌ Input file not found: ${config.input}`);
    return false;
  }

  const markdown = fs.readFileSync(config.input, 'utf-8');

  // Convert markdown to HTML
  const contentHtml = marked.parse(markdown);

  // Build complete HTML document
  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  ${getStyles(config.watermark)}
</head>
<body>
  ${generateCoverPage(config)}
  ${contentHtml}
  ${generateFooter(config)}
</body>
</html>
  `;

  // Ensure output directory exists
  const outputDir = path.dirname(config.output);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Launch Puppeteer and generate PDF
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  await page.setContent(html, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: config.output,
    format: 'Letter',
    printBackground: true,
    displayHeaderFooter: false, // We're using CSS for footer
    margin: {
      top: '1in',
      right: '0.75in',
      bottom: '1in',
      left: '0.75in'
    }
  });

  await browser.close();

  console.log(`   ✅ PDF generated successfully`);
  return true;
}

// Main execution
async function main() {
  console.log('🔱 OMEGA Whitepaper PDF Generator');
  console.log('==================================\n');

  let successCount = 0;
  let failCount = 0;

  for (const config of WHITEPAPERS) {
    const success = await generatePDF(config);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
  }

  console.log('\n==================================');
  console.log(`✅ Success: ${successCount}`);
  console.log(`❌ Failed:  ${failCount}`);
  console.log('==================================\n');

  process.exit(failCount > 0 ? 1 : 0);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
