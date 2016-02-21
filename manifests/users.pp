class users {
   user { "jrivero":
       ensure     => 'present',
       shell      => '/bin/bash',
       managehome => 'true',
       groups     => 'sudo',
   }
}
