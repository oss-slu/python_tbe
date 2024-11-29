#include "../tbe_batch_processor.h"
#include <assert.h>

int main() {
    TBE_Metadata metadata;
    process_tbe_file("../sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv", &metadata);
    assert(metadata.record_count > 0);

    process_tbe_directory("../sample_data");
    return 0;
}