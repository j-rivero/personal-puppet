$confdir_setting = $settings::confdir
class files {

  define delete_lines($file, $pattern) {
    exec { "/bin/sed -i -r -e '/$pattern/d' $file":
        onlyif => "/bin/grep -E '$pattern' '$file'",
    }
  }

  file_line { "/etc/sudoers":
    ensure => present,
    line   => 'jrivero ALL=(ALL) NOPASSWD:ALL',
    path   => '/etc/sudoers',
  }
}
