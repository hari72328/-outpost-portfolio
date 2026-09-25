// Render each page of a resume PDF to out/resume-page-N.png for the resume
// panel, which shows the CV as images (the page cannot embed a PDF or use an
// iframe). macOS only, no dependencies: it drives the PDFKit that ships with
// the OS through JavaScript for Automation. Run it from the project folder:
//
//     osascript -l JavaScript gen/resume_pages.js ~/Downloads/new-resume.pdf
//
// Pages are drawn at 3x their point size, sharp at the panel width on a
// retina screen.
ObjC.import('AppKit');
ObjC.import('PDFKit');

function run(argv) {
  const here = $.NSString.stringWithString($.NSProcessInfo.processInfo.environment.objectForKey('PWD')).js;
  if (!argv.length) throw new Error('usage: osascript -l JavaScript gen/resume_pages.js <resume.pdf>');
  const pdf = $.NSString.stringWithString(argv[0]).stringByExpandingTildeInPath.js;
  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(pdf));
  if (doc.isNil()) throw new Error('cannot open ' + pdf);
  const scale = 3, out = [];
  for (let i = 0; i < doc.pageCount; i++) {
    const page = doc.pageAtIndex(i);
    const box = page.boundsForBox($.kPDFDisplayBoxMediaBox);
    const w = Math.round(box.size.width * scale), h = Math.round(box.size.height * scale);
    const rep = $.NSBitmapImageRep.alloc.initWithBitmapDataPlanesPixelsWidePixelsHighBitsPerSampleSamplesPerPixelHasAlphaIsPlanarColorSpaceNameBytesPerRowBitsPerPixel(
      null, w, h, 8, 4, true, false, $.NSDeviceRGBColorSpace, 0, 0);
    const ctx = $.NSGraphicsContext.graphicsContextWithBitmapImageRep(rep);
    $.NSGraphicsContext.saveGraphicsState;
    $.NSGraphicsContext.setCurrentContext(ctx);
    $.NSColor.whiteColor.setFill;
    $.NSRectFill($.NSMakeRect(0, 0, w, h));
    const xf = $.NSAffineTransform.transform;
    xf.scaleBy(scale);
    xf.translateXByYBy(-box.origin.x, -box.origin.y);
    xf.concat;
    page.drawWithBoxToContext($.kPDFDisplayBoxMediaBox, ctx.CGContext);
    $.NSGraphicsContext.restoreGraphicsState;
    const file = here + '/out/resume-page-' + (i + 1) + '.png';
    rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $({})).writeToFileAtomically(file, true);
    out.push('wrote ' + file + ' (' + w + 'x' + h + ')');
  }
  return out.join('\n');
}
