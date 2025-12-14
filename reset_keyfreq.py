from pathlib import Path
import json
import sys

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
    