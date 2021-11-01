/* =============================================================================
	jQuery Textarea Auto Height 1.0.0
	Copyright(c) 2016, ShanaBrian
	Dual licensed under the MIT and GPL licenses.
============================================================================= */
(function($) {
	var changeValueIntervalId;

	var changeValueFunction = function(element) {
		var $element     = $(element),
			stockValue   = '',
			currentValue = '';

		if ($element.length === 0) return;

		changeValueIntervalId = setInterval(function() {
			stockValue   = $element.data('stockValue');
			currentValue = $element.val();

			if (stockValue !== currentValue) {
				$element.data('stockValue', currentValue);
				$element.trigger('changeValue');
			}
		}, 10);
	};

	$.event.special.changeValue = {
		add : function(event) {
			changeValueFunction(this, event.data);
		},
		remove : function(event) {
			clearInterval(changeValueIntervalId);
		}
	};
})(jQuery);

(function($) {

	$.fn.textareaAutoHeight = function(options) {
		if ($(this).length === 0) {
			return this;
		}

		if ($(this).length > 1) {
			$.each(this, function() {
				$(this).textareaAutoHeight(options);
			});
			return this;
		}

		var $element = this,
			settings = {};

		// 初期化
		var init = function() {
			/*
				auto : 自動的に高さを揃えるかどうか [ true | false ]
			*/
			settings = $.extend({
				auto : true
			}, options);

			if ($element.get(0).tagName.toLowerCase() !== 'textarea') return;

			setup();
		};

		// セットアップ
		var setup = function() {
			var $stockTextarea = $('<pre><code></code></pre>'),
				height         = Number($element.height()),
				setCSS         = {
				'width'          : Number($element.width()),
				'margin'         : '0',
				'padding-top'    : Number($element.css('paddingTop').replace('px', '')),
				'padding-left'   : Number($element.css('paddingLeft').replace('px', '')),
				'padding-right'  : Number($element.css('paddingRight').replace('px', '')),
				'padding-bottom' : Number($element.css('paddingBottom').replace('px', '')),
				'box-sizing'     : Number($element.css('box-sizing')),
				'font-size'      : Number($element.css('font-size').replace('px', '')),
				'font-family'    : $element.css('font-family'),
				'line-height'    : Number($element.css('line-height').replace('px', '')) + 'px',
				'letter-spacing' : Number(($element.css('letter-spacing')) ? $element.css('letter-spacing').replace('px', '') : 0) + 'px',
				'text-align'     : $element.css('text-align'),
				'white-space'    : 'pre-wrap',
				'word-wrap'      : 'break-word'
			};

			$stockTextarea.css(setCSS).hide();
			$stockTextarea.find('code').css($.extend(setCSS, {
				'padding-top'    : 0,
				'padding-left'   : 0,
				'padding-right'  : 0,
				'padding-bottom' : 0,
				'width'          : 'auto'
			}));

			$element.css({
				'resize'   : 'none',
				'overflow' : 'hidden'
			});

			$element.data('defaultHeight', height);
			$element.data('stockObj', $stockTextarea);

			$('body').append($stockTextarea);
			resizeTextarea();

			if (settings.auto === true) {
				$element.on('changeValue', function() {
					resizeTextarea();
				});
			}
		};

		// テキストエリアの高さ調整
		var resizeTextarea = function() {
			$element.scrollTop(0);

			setTimeout(function() {
				var $stockObj     = $element.data('stockObj'),
					stockHeight   = Number($stockObj.height()),
					defaultHeight = $element.data('defaultHeight'),
					doc           = $element.val().replace(/\r/g, '');

				if (navigator.userAgent.toLowerCase().indexOf('msie 7.0') !== -1) {
					doc = doc.replace(/\n/g, '\r\n');
				}

				$stockObj.find('code').empty().text(doc + '\n');

				if (stockHeight > defaultHeight) {
					$element.height(stockHeight);
				} else {
					$element.height(defaultHeight);
				}

				resizeTextarea();
			}, 10);
		};

		// テキストエリアの高さ調整（メソッド）
		$element.resizeTextarea = function() {
			resizeTextarea();
		};

		init();

		return this;
	};
})(jQuery);
