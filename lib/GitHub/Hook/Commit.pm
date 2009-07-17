package GitHub::Hook::Commit;
use Coat;

has id        => (isa => 'Str');
has url       => (isa => 'Str');
has author    => (isa => 'Str');
has message   => (isa => 'Str');
has timestamp => (isa => 'Str');

'GitHub::Hook::Commit';
