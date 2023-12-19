#include "delta_r_matching.h"

void fill_with_best_indicies(
	bool* reconstruction_successful,
	int* indicies,
	int number_of_jets,
	PtEtaPhiEVector* jet_lvectors,
	PtEtaPhiMVector wboson1_decay1_lvector,
	PtEtaPhiMVector wboson1_decay2_lvector,
	PtEtaPhiMVector wboson2_decay1_lvector,
	PtEtaPhiMVector wboson2_decay2_lvector,
	PtEtaPhiMVector bquark1_lvector,
	PtEtaPhiMVector bquark2_lvector
)
{		
	// set of unavalable indicies (jets that have already been matched)
	std::unordered_set<int> unavailable_indicies;


	// find best match for each truth object
	indicies[0] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, wboson1_decay1_lvector);
	indicies[1] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, wboson1_decay2_lvector);
	indicies[2] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, wboson2_decay1_lvector);
	indicies[3] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, wboson2_decay2_lvector);
	indicies[4] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, bquark1_lvector);
	indicies[5] = find_best_match(&unavailable_indicies, number_of_jets, jet_lvectors, bquark2_lvector);


	// check whether matching was successful or not
	*reconstruction_successful = false;
	if(number_of_jets<6)
		return; // unsuccessful, not enough jets for all truth objects

	for(int i=0; i<6; i++){ 
		if(indicies[i]==-1)
			return; // unsuccessful, not every truth object has a matching jet index
	}

	*reconstruction_successful = true; // successful matching
}

int find_best_match(
	std::unordered_set<int>* unavailable_indicies,
	int number_of_jets,
	PtEtaPhiEVector* jet_lvectors,
	PtEtaPhiMVector truth_object_lvector
)
{
	float best_delta_R = 999;
	int best_delta_R_index = -1;

	for(int current_index=0; current_index<number_of_jets; current_index++){
		if(unavailable_indicies->count(current_index)>0) // if unavailable, skip
			continue;

		float delta_R = calc_delta_R(truth_object_lvector.Eta(), truth_object_lvector.Phi(), jet_lvectors[current_index].Eta(), jet_lvectors[current_index].Phi() );
		if( (delta_R<best_delta_R) && (delta_R<=DELTA_R_THRESHOLD) ){ // must be better than previous match and below threshold
			best_delta_R = delta_R;
			best_delta_R_index = current_index;
		}
	}

	unavailable_indicies->insert(best_delta_R_index); // index was matched, add to unavailable indicies for next matching proccess
	return best_delta_R_index;
}

float calc_delta_R(Float_t eta1, Float_t phi1, Float_t eta2, Float_t phi2){
	return sqrt( (eta2-eta1)*(eta2-eta1) + (phi2-phi1)*(phi2-phi1) );
}
