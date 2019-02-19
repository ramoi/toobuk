		selectList = source.select( self.__pattern__.get('selector') )

		if not pattern.get('slice') is None :
			start = pattern['slice']['start'] if pattern['slice'].get('start') is not None else 0
			end = pattern['slice']['end'] if pattern['slice'].get('end') is not None else len(selectList)
			selectList = selectList[start:end]

		for index, select in enumerate(selectList) :
			if len(result) < index + 1:
				result.append({})

			#addData(index, select)
			self._addData_( result[index], select) 