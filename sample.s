        INP
        STA numOne
        INP
        STA two

loop	LDA total
		ADD numOne
		STA total
		LDA two
		SUB ONE
		STA two
		BRP loop
		LDA total
		SUB numOne
		STA total
        LDA total
        OUT

		numOne DAT 0
		two DAT 0
		total DAT 0
		ONE DAT 1