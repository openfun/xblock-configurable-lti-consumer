function configurableLTIConsumerXblockIframeResizerInit(runtime, element, json_args) {
    var $element = $("#" + json_args["element_id"]);
    LtiConsumerXBlock();  // call inherited lti_consumer javascript initialization
    var $iframe = $element.find('iframe');
    var $div = $element.find("div");
    var automatic_resizing = $div.data('automatic-resizing') === "True"?true:false;
    var inline_ratio = parseFloat($div.data('inline-ratio')) || false;
    var inline_height = parseFloat($div.data('inline-height')) || false;
    var width = $('.content-primary,.vert-mod').width();

    if (automatic_resizing) {
        $iframe.iFrameResize({ // Initialize IframeResizer on lti_consumer iframe
            checkOrigin: false,
            log: false
        });
    }
    if (inline_ratio) {
        var estimated_height = width * inline_ratio;
        $iframe.height(estimated_height);
    } else if (inline_height) {
        $iframe.height(inline_height);
    }
};

