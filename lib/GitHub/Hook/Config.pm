package GitHub::Hook::Config;
use Coat;

has smtp_host    => (isa => 'Str');
has repositories => (isa => 'ArrayRef');

'GitHub::Hook::Config';
