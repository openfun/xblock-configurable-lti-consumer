function configurableLTIConsumerXblockIframeResizerInit() {
    $(function ($) {
        LtiConsumerXBlock();  // call inherited lti_consumer javascript initialization
        $('.ltiLaunchFrame').iFrameResize({ // Initialize IframeResizer on lti_consumer iframe class
            checkOrigin: false,
            log: false
        })
    });
};