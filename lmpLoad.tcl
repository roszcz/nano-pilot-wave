proc lmpLoad {args} {
    if {$args == ""} {
        puts "Usage: lmpLoad filename args "
        puts "  args:"
        puts "    vmdField (beta user, user1 ..)  dumpField (0-N)"

        puts ""
        return
    }

    set fileName [lindex $args 0]
    if {[file exists $fileName] != 1} {
        puts ""
        puts "File $fileName does not exist"
        puts ""
        return
    }

    set beta -1
    set user -1
    set user2 -1
    set user3 -1
    set user4 -1
    foreach {field collN} [lrange $args 1 end] {
        if {$field == "beta"} {
            set beta $collN
        }
        if {$field == "user"} {
            set user $collN
        }
        if {$field == "user2"} {
            set user2 $collN
        }
        if {$field == "user3"} {
            set user3 $collN
        }
        if {$field == "user4"} {
            set user4 $collN
        }
    }
    
    set nFrames [molinfo top get numframes]
    set nAtoms [molinfo top get numatoms]
    
    set fileIn [open $fileName r]
    for {set j 0} {$j < $nFrames} {incr j} {
        gets $fileIn line ;# ITEM: TIMESTEP
        gets $fileIn line ;# --
        puts $line
        
        gets $fileIn line ;# ITEM: NUMBER OF ATOMS
        gets $fileIn line ;# --
        gets $fileIn line ;# ITEM: BOX BOUNDS ff ff ff
        gets $fileIn line ;# --
        gets $fileIn line ;# --
        gets $fileIn line ;# --
        gets $fileIn line ;# ITEM: ATOMS 

        
        set system [atomselect top "all" frame $j]
        if {$beta >= 0} {
            set betaList [list]
        }
        if {$user >= 0} {
            set userList [list]
        }
        if {$user2 >= 0} {
            set user2List [list]
        }
        if {$user3 >= 0} {
            set user3List [list]
        }
        if {$user4 >= 0} {
            set user4List [list]
        }
        for {set i 0} {$i < $nAtoms} {incr i} {
            gets $fileIn line ;# 0 1 2...
            if {$beta >= 0} {
                lappend betaList [expr double([lindex $line $beta])]
            }
            if {$user >= 0} {
                lappend userList [expr double([lindex $line $user])]
            }
            if {$user2 >= 0} {
                lappend user2List [expr double([lindex $line $user2])]
            }
            if {$user3 >= 0} {
                lappend user3List [expr double([lindex $line $user3])]
            }
            if {$user4 >= 0} {
                lappend user4List [expr double([lindex $line $user4])]
            }
        }
        if {$beta >= 0} {
            $system set beta $betaList
        }
        if {$user >= 0} {
            $system set user $userList
        }
        if {$user2 >= 0} {
            $system set user2 $user2List
        }
        if {$user3 >= 0} {
            $system set user3 $user3List
        }
        if {$user4 >= 0} {
            $system set user4 $user4List
        }
        $system delete
    }
    close $fileIn
}

# run default for this script

lmpLoad pilotwaves.lammpstrj user2 4
