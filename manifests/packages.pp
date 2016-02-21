class packages {
 $enhancers = [ 'screen', 
                'strace', 
		'sudo', 
		'gvim', 
		'cmake', 
		'git', 
		'mercurial',
                'bash-completion',
                's3cmd',
                'curl',
                'wget',
                'locales',
                'gdb']
 package { $enhancers: ensure => 'installed' }

 # Docker support. Ubuntu packages are outdated, using docker ones
 case $operatingsystemrelease {
   12.04 : {
       exec {'no-docker-script':
           command => "echo 'No docker on Precise'"
       }
   }
   default : {
       package { "wget" : ensure => installed }
       exec {'docker-script':
           command => "/usr/bin/curl -sSL https://get.docker.io/ubuntu/ | sudo sh",
       }

       exec {'gazebo-script':
           command => "/usr/bin/curl -sSL http://get.gazebosim.org | sudo sh",
       }

       package { "qemu-user-static"  : ensure => installed }
   }
 }
}
