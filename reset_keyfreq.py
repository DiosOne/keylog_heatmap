# Copyright (C) 2025 Dom Andrewartha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

def main() -> None:
    base_dir= Path(__file__).parent
    keyfreq_path= base_dir/'heatmap'/'keyfreq.json'
    
    prompt= (
        'Warning this will reset your merged frequency data.'
        'Session files remain intact. Proceed? [y/n]: '
    )
    answer= input(prompt).strip().lower()
    if answer not in {'y', 'yes'}:
        print('Aborted; frequency data unchanged.')
        return
    
    keyfreq_path.write_text('{}\n', encoding='utf-8')
    print(f"Reset {keyfreq_path} to empty {{}}")
    
if __name__=='__main__':
    main()
    