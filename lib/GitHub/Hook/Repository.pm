package GitHub::Hook::Repository;
use Coat;

has owner => (isa => 'Str');
has url   => (isa => 'Str');
has name  => (isa => 'Str');

'GitHub::Hook::Repository';
