#==============================================================================
# ** HTTP
#------------------------------------------------------------------------------
#  This module is for HTTP responses.
#==============================================================================

module HTTP

  @responses = {
    0 => 'Unknown',
    # 100..199: Informational responses
    100 => 'Continue',
    101 => 'Switching Protocol',
    102 => 'Processing', # WebDAV
    103 => 'Early Hints',
    # 200..299: Successful responses
    200 => 'OK',
    201 => 'Created',
    202 => 'Accepted',
    203 => 'Non-Authoritative Information',
    204 => 'No Content',
    205 => 'Reset Content',
    206 => 'Partial Content',
    207 => 'Multi-Status',
    208 => 'Already Reported', # WebDAV
    226 => 'IM Used', # HTTP Delta encoding
    # 300..399: Redirection messages
    300 => 'Multiple Choice',
    301 => 'Moved Permanently',
    302 => 'Found',
    303 => 'See Other',
    304 => 'Not Modified',
    305 => 'Use Proxy', # Deprecated
    307 => 'Temporary Redirect',
    308 => 'Permanent Redirect',
    # 400..499: Client error responses
    400 => 'Bad Request',
    401 => 'Unauthorized',
    402 => 'Payment Required',
    403 => 'Forbidden',
    404 => 'Not Found',
    405 => 'Method Not Allowed',
    406 => 'Not Acceptable',
    407 => 'Proxy Authentication Required',
    408 => 'Request Timeout',
    409 => 'Conflict',
    410 => 'Gone',
    411 => 'Length Required',
    412 => 'Precondition Failed',
    413 => 'Payload Too Large',
    414 => 'URI Too Long',
    415 => 'Unsupported Media Type',
    416 => 'Range Not Satisfiable',
    417 => 'Expectation Failed',
    418 => 'I\'m a teapot',
    421 => 'Misdirected Request',
    422 => 'Unprocessable Entity', # WebDAV
    423 => 'Locked', # WebDAV
    424 => 'Failed Dependency', # WebDAV
    425 => 'Too Early',
    426 => 'Upgrade Required',
    428 => 'Precondition Required',
    429 => 'Too Many Requests',
    431 => 'Request Header Fields Too Large',
    451 => 'Unavailable For Legal Reasons',
    # 500..599: Server error responses
    500 => 'Internal Server Error',
    501 => 'Not Implemented',
    502 => 'Bad Gateway',
    503 => 'Service Unavailable',
    504 => 'Gateway Timeout',
    505 => 'HTTP Version Not Supported',
    506 => 'Variant Also Negotiates',
    507 => 'Insufficient Storage', # WebDAV
    508 => 'Loop Detected', # WebDAV
    510 => 'Not Extended',
    511 => 'Network Authentication Required'
  }.freeze

  def self.codename(http_code)
    if @responses.has_key?(http_code)
      return @responses[http_code]
    else
      raise TypeError, 'Invalid HTTP code'
    end
  end

  def self.response(code = 200, content = '')
    return [
      "HTTP/1.1 #{code} #{self.codename(code)}",
      "Connection: close",
      "Content-Type: text/plain; charset=utf-8",
      "Content-Length: #{content.length + 1}",
      "Date: #{Time.now.gmtime.strftime('%a, %d %b %Y %T GMT')}",
      "Server: NikosPancakes/1.0",
      "",
      content.to_s + "\n"
    ].join("\r\n")
  end

  def self.response_data(code = 200, data = '', mimetype = '')
    return [
      "HTTP/1.1 #{code} #{self.codename(code)}",
      "Connection: close",
      "Content-Type: #{mimetype}",
      "Content-Length: #{data.length}",
      "Date: #{Time.now.gmtime.strftime('%a, %d %b %Y %T GMT')}",
      "Server: NikosPancakes/1.0",
      "",
      data
    ].join("\r\n")
  end

end
