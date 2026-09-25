// Render each page of resume/resume.pdf to out/resume-page-N.png for
// the Simple View, which shows the real CV as images (the artboard cannot embed a
// PDF or use an iframe). macOS only, no dependencies: it drives the PDFKit that
// ships with the OS through JavaScript for Automation.
//
//     osascript -l JavaScript gen/resume_pages.js
//
// Pages are drawn at 3x their point size, sharp at the Simple View width on a
// retina screen.
ObjC.import('AppKit');
ObjC.import('PDFKit');

function run() {
  const here = $.NSString.stringWithString($.NSProcessInfo.processInfo.environment.objectForKey('PWD')).js;
  const pdf = here + '/resume/resume.pdf';
  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(pdf));
  if (doc.isNil()) throw new Error('cannot open ' + pdf + ' (run this from the project root)');
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
